from datetime import datetime
from uuid import UUID, uuid4
from logging import getLogger
from django.utils import timezone
from django.db.models import QuerySet
from typing import Any, NoReturn

from chat.models import Room
from accounts.models import CustomUser


logger = getLogger(__name__)


"""
uuidStringをUUIDに変換
"""
def str_to_uuid(str_uuid:str) -> UUID:
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
        if type(id) is key_type:
            output.append(id)
    return output


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


def create_room_object(room_name:str, 
                       u_instance:CustomUser) -> Room|None:
        new_roomid = uuid4()
        try:
            new_room = Room.objects.create(room_id=new_roomid, room=room_name, owner=u_instance, created_at=timezone.now())
        except Exception as e:
            logger.warn(e)
            return None
        if update_customuser_model({'joined_room':new_roomid}, u_instance=u_instance):
            return new_room
        else:
            new_room.delete()
            return None


def create_guestuser_object(username:str, room_uuid:UUID) -> CustomUser:
    try:
        obj = CustomUser.objects.create_guestuser(username = username, joined_room=room_uuid)
    except Exception as e:
        logger.warn(e)
        return None
    return obj


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


# Roomモデルが削除された後に、参加しているゲストCustomUserモデルを削除
def post_room_object_deleted(room_uuid:UUID) -> NoReturn:
    from ..tasks import delete_guest_accounts_delayed
    delete_guest_accounts_delayed.delay(room_uuid)