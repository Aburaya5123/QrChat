from datetime import datetime
from uuid import UUID, uuid4
from logging import getLogger
from django.utils import timezone
from django.db.models import QuerySet
from typing import Any

from chat.models import Room, RoomMessage
from accounts.models import CustomUser


logger = getLogger(__name__)


"""
uuidStringをUUIDに変換
"""
def str_to_uuid(str_uuid:str) -> UUID|None:
    try:
        shaped_strs = str_uuid.strip('/').split('/')
        output = UUID(shaped_strs[0])
    except Exception as e:
        logger.error(e)
        return None
    return output

"""
keyの値をkey_typeに変換し、listに格納して返す
"""
def convert_type(key:Any|list[Any], 
                 key_type:type) -> list[Any]:
    output = []
    if type(key) is not list:
        key = [key]
    for id in key:
        if key_type is str:
            if id is not str:
                id = str(id)
        elif key_type is UUID:
            if type(id) is str:
                id = str_to_uuid(id)
            elif type(id) is not UUID:
                raise ValueError(f"Invalid value type.")
        else:
            raise ValueError(f"Input type:{key_type} is not implemented.")
        if type(id) is key_type:
            output.append(id)
    return output

"""
CustomUserモデルから条件に一致するオブジェクトを検索する。

get_instance: Bool  該当するオブジェクトが見つかった際に、オブジェクトを返す場合はTrue
"""
def find_customuser_object(get_instance:bool, 
                           user_id:UUID|list[UUID]=None, 
                           username:str|list[str]=None, 
                           login_id:str|list[str]=None, 
                           last_login:datetime=None, 
                           joined_room:UUID|list[UUID]=None, 
                           is_superuser:bool=None, 
                           is_active:bool=None, 
                           is_guest:bool=None) -> QuerySet[CustomUser]|None:
    conditions = {}
    if user_id is not None:
        conditions['user_id__in'] = convert_type(user_id, UUID)
    if username is not None:
        conditions['username__in'] = convert_type(username, str)
    if login_id is not None:
        conditions['login_id__in'] = convert_type(login_id, str)
    if last_login is not None:
        conditions['last_login'] = last_login
    if joined_room is not None:
        conditions['joined_room__in'] = convert_type(joined_room, UUID)
    if is_superuser is not None:
        conditions['is_superuser'] = is_superuser
    if is_active is not None:
        conditions['is_active'] = is_active
    if is_guest is not None:
        conditions['is_guest'] = is_guest

    if get_instance:
        results = CustomUser.objects.filter(**conditions)
        if results.count() == 0:
            return None
        else:
            return results
    else:
        return CustomUser.objects.filter(**conditions).exists()

def create_customuser_object(login_id:str, 
                             pw:str) -> CustomUser|None:
    try:
        obj = CustomUser.objects.create_user(login_id=login_id, password=pw)
    except Exception as e:
        logger.warn(e)
        return None
    return obj

def create_guestuser_object(username:str, room_uuid:UUID) -> CustomUser:
    try:
        obj = CustomUser.objects.create_guestuser(username = username, joined_room=room_uuid)
    except Exception as e:
        logger.warn(e)
        return None
    return obj

"""
CustomUserモデルの更新
更新するオブジェクトは、u_instance,u_pkのいずれかで指定

key_value_dict:dict[str,str] 更新する項目のキー,値を格納
"""
def update_customuser_model(key_value_dict:dict[str,str], 
                            u_instance:CustomUser=None, 
                            u_pk:UUID=None) -> bool:
    if u_instance is None:
        if u_pk is None:
            raise ValueError("Specify either the instance or the primary key of the model to update.")
        try:
            u_instance = CustomUser.objects.get(pk=u_pk)
        except CustomUser.DoesNotExist:
            logger.warn(f"CustomUser<{u_pk}> Not Found.")
            return False

    for key, value in key_value_dict.items():
        setattr(u_instance, key, value)
    u_instance.save()
    return True

"""
Roomモデルから条件に一致するオブジェクトを検索する。

get_instance: Bool  該当するオブジェクトが見つかった際に、オブジェクトを返す場合はTrue
"""
def find_room_object(get_instance:bool,
                     room_id:UUID|list[UUID]=None, 
                     room:str|list[str]=None, 
                     owner:UUID|list[UUID]=None, 
                     created_at:datetime=None) -> QuerySet[Room]|None:
    conditions = {}
    if room_id is not None:
        conditions['room_id__in'] = convert_type(room_id, UUID)
    if room is not None:
        conditions['room__in'] = convert_type(room, str)
    if owner is not None:
        conditions['owner__in'] = convert_type(owner, UUID)
    if created_at is not None:
        conditions['created_at'] = created_at

    if get_instance:
        results = Room.objects.filter(**conditions)
        if results.count() == 0:
            return None
        else:
            return results
    else:
        return Room.objects.filter(**conditions).exists()

"""
有効期限切れのルームモデルのクエリを返す
"""
def find_expired_room() -> QuerySet[Room]|None:
    result = Room.objects.filter(expire_at__lt=timezone.now())
    return None if result.count()==0 else result

def create_room_object(room_name:str, 
                       u_instance:CustomUser) -> Room|None:
        new_roomid = uuid4()
        try:
            new_room = Room(room_id=new_roomid,
                            room=room_name,
                            owner=u_instance,
                            created_at=timezone.now())
            new_room.set_expire_date()
            new_room.save()
        except Exception as e:
            logger.warn(e)
            return None
        if update_customuser_model({'joined_room':new_roomid}, u_instance=u_instance):
            return new_room
        else:
            new_room.delete()
            return None

"""
Roomモデルが削除された後に、参加しているゲストCustomUserモデルを削除
"""
def post_room_object_deleted(room_uuid:UUID) -> None:
    from ..tasks import delete_guest_accounts_delayed
    delete_guest_accounts_delayed.delay(room_uuid)


def delete_room_model(room_id:UUID) -> bool:
    try:
        room_object = Room.objects.get(pk=room_id)
        room_object.delete()
    except Room.DoesNotExist:
        return False
    return True

"""
過去のチャット履歴の取得

room_uuid:UUID 該当ルーム
"""
def get_historical_chat_messages(room_uuid:UUID) -> dict|None:
    chats = RoomMessage.objects.filter(room=room_uuid)
    if chats.count()==0:
        return None
    output={}
    # 最大取得件数 = 50
    if chats.count()>50:
        chats = list(chats)[-50:]

    for chat in chats:
        output[str(chat.chat_id)] = {'name':chat.name, 
                                     'content':chat.content, 
                                     'created_at':str(chat.created_at),
                                     'icon':chat.icon}
    # 作成日時で昇順
    sorted(output.items(), key=lambda value: value[1]['created_at'])

    return output

"""
チャット履歴の作成
オブジェクトの作成に成功した場合Trueを返す
"""
def create_room_messages(sender:str,
                         content:str,
                         created_at:datetime,
                         room_uuid:UUID,
                         icon:str) -> bool:
    room = find_room_object(True, room_id=room_uuid)
    if room is None:
        return False
    _ = RoomMessage.objects.create(pk=uuid4(), 
                                   room=room.first(), 
                                   name=sender, 
                                   content=content, 
                                   created_at=created_at,
                                   icon=icon)
    return True

"""
Channelに接続中のユーザーを更新

connected:Bool Websocket接続時にTrueとする
"""
def channel_consumer_update(connected: bool,
                            room_id: UUID,
                            user: CustomUser) -> int:
    room = find_room_object(True, room_id=room_id)
    if room is None:
        return 0
    channel = room.first()

    try:
        if connected:
            channel.add_member(user)
        else:
            channel.remove_member(user)
    except Exception as e:
        logger.warn(e)
    return channel.member_count