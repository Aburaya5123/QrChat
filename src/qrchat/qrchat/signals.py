
from django.db.models.signals import post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from chat.models import Room
from .utils.model_helper import post_room_object_deleted


# Roomのモデルの削除後に、Websocketに通知メッセージを送信
@receiver(post_delete, sender=Room)
def model_update(sender, instance:Room, **kwargs):
    # ルームが閉じることを参加者に通知
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(str(instance.room_id), {
        'type': 'send.data',
        'data': {
            'room-closed': 'Close.'
        }
    })
    """
    post_room_object_deleted(instance.room_id)