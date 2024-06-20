from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from logging import getLogger
from django.utils import timezone
from datetime import timedelta
import os

from accounts.models import CustomUser, MAX_USERNAME_LENGTH


# ルーム名の最大文字数
MAX_ROOMNAME_LENGTH = 30


logger = getLogger(__name__)


# ルーム管理モデル
class Room(models.Model):

    # ルームの寿命を指定(day)
    EXPIRE_PERIOD = 5

    room_id = models.UUIDField(primary_key=True, default=uuid4)
    room = models.CharField(verbose_name=_("ルーム名"), unique=False, blank=False, null=False,
                        max_length=MAX_ROOMNAME_LENGTH, validators=[MinLengthValidator(1)])
    owner = models.ForeignKey(
        CustomUser,
        related_name='room_owner',
        on_delete=models.CASCADE # Userオブジェクトと連動して削除
    )
    created_at = models.DateTimeField(auto_created=True) # ルーム作成日時
    expire_at = models.DateTimeField(null=True)    
    participants = models.ManyToManyField(to='accounts.CustomUser')
    qrcode = models.CharField(verbose_name=_("QRCode"), unique=False, blank=True, null=True,
                              max_length=200)

    # ルーム参加者の追加
    def add_member(self, user) -> None:
        self.participants.add(user)

    # ルーム参加者の削除
    def remove_member(self, user) -> None:
        try:
            self.participants.remove(user)
        except Exception as e:
            logger.error(e)

    # ルーム参加者取得
    @property
    def member_count(self) -> int:
        return len(self.participants.all())
    
    def save(self, *args, **kwargs) -> None:
        # QRコードの作成
        from accounts.middleware import PathPattern
        from qrchat.settings import CURRENT_DOMAIN_NAME

        room_url = CURRENT_DOMAIN_NAME + PathPattern.path_pattern['lobby'] + str(self.room_id)

        if os.getenv("REMOTE_DEPLOY", False):
            from qrchat.publish_messages import create_qrcode
            self.qrcode = create_qrcode(room_url, self.room_id)
        else:
            from qrchat.qrcode_generator import generate_qrcode
            self.qrcode = generate_qrcode(room_url, self.room_id)

        super().save(*args, **kwargs)

    def set_expire_date(self):
        self.expire_at = timezone.now() + timedelta(days=self.EXPIRE_PERIOD)

    def __str__(self) -> str:
        return str(self.room_id)
        

# チャットメッセージ管理モデル
class RoomMessage(models.Model):
    chat_id = models.UUIDField(primary_key=True, default=uuid4)
    room = models.ForeignKey(
        Room,
        related_name='roomid',
        on_delete=models.CASCADE # Roomオブジェクトと連動して削除
    )
    name = models.CharField(unique=False, default=_("名無し"), max_length=MAX_USERNAME_LENGTH) # 発言者のユーザー名
    content = models.TextField() # 発言内容
    created_at = models.DateTimeField(auto_created=True) # 発言日時
    icon = models.CharField(unique=False, blank=False, null=False, max_length=10)

    def __str__(self) -> str:
        return str(self.chat_id)