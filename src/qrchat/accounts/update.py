from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.sessions.models import Session
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from logging import getLogger
from uuid import UUID

from qrchat.utils.model_helper import find_expired_room, find_customuser_object


logger = getLogger(__name__)


def start():
    scheduler = BackgroundScheduler()
    # 実行間隔
    scheduler.add_job(periodic_task, 'interval', minutes=30)
    scheduler.start()

# APSSchedulerで定期実行
def periodic_task() -> None:
    delete_expired_sessions()
    delete_expired_room()  

# 有効期限切れのセッションの削除
def delete_expired_sessions() -> None:
    try:
        expired_session = Session.objects.filter(expire_date__lt=timezone.now())
    except Exception as e:
        logger.warn(e)
    if expired_session.count() == 0:
        return
    # セッション有効期限が過ぎているユーザーID(str)を格納
    pks = []
    for expired in expired_session:
        uid = expired.get_decoded().get('_auth_user_id')
        pks.append(uid)

    if len(pks) > 0:
        # WebSocketから切断
        expired_users = find_customuser_object(True, user_id=pks)
        if expired_users is not None:
            for u in expired_users:
                if type(u.joined_room) is UUID:
                    disconnect_ws_user(u.joined_room, u.user_id)

        # ゲストアカウントの場合に限りモデルオブジェクト削除
        expired_guests = find_customuser_object(True, user_id=pks, is_guest=True)
        if expired_guests is not None:
            #print(f"Delete Expired Guest Accounts. \
            #      Total:{expired_guests.count()} TimeStamp:{timezone.now()}")
            expired_guests.delete()
    expired_session.delete()

# WebsocketからSessionの切れたユーザーを切断
def disconnect_ws_user(room_id:UUID, user_id:UUID) -> None:
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(str(room_id), {
        'type':'disconnect_user',
        'user_id':str(user_id),
        'code':419
    })

# 有効期限切れのルームの削除
def delete_expired_room() -> None:
    expired = find_expired_room()
    if expired is None:
        return
    #print(f"Delete Expired Rooms. \
    #    Total:{expired.count()} TimeStamp:{timezone.now()}")
    expired.delete()