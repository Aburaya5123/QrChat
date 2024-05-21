from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from uuid import uuid4

from accounts.models import CustomUser


# ルーム管理モデル
class Room(models.Model):
    room_id = models.UUIDField(primary_key=True, default=uuid4)
    room = models.CharField(verbose_name=_("ルーム名"), unique=False, blank=False, null=False,
                        max_length=30, validators=[MinLengthValidator(1)])
    owner = models.ForeignKey(
        CustomUser,
        blank=True,
        null=True,
        related_name='room_owner',
        on_delete=models.CASCADE # Userオブジェクトと連動して削除
    )
    created_at = models.DateTimeField(auto_created=True) # ルーム作成日時
        

# チャットメッセージ管理モデル
class RoomMessage(models.Model):
    chatid = models.UUIDField(primary_key=True, default=uuid4)
    room = models.ForeignKey(
        Room,
        blank=True,
        null=True,
        related_name='roomid',
        on_delete=models.CASCADE # Roomオブジェクトと連動して削除
    )
    name = models.CharField(max_length=30) # 発言者のユーザー名
    content = models.TextField() # 発言内容
    created_at = models.DateTimeField(auto_created=True) # 発言日時