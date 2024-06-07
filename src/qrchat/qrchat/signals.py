
from django.db.models.signals import post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from uuid import UUID

from chat.models import Room
from .utils.model_helper import post_room_object_deleted


# channe-groupの削除, ゲストユーザーモデルの削除
@receiver(post_delete, sender=Room)
def room_deleted(sender, instance:Room, **kwargs):
    send_closure_signal(instance.room_id)
    post_room_object_deleted(instance.room_id)

# ルームが閉じることをWebsocketで通知
def send_closure_signal(room_id:UUID) -> None:
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(str(room_id), {
        'type': 'system_notification',
        'code': 410
    })