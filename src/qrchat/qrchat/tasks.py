from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
from uuid import UUID
from typing import NoReturn

from .utils.model_helper import find_customuser_object


# CustomUserモデルからゲストを削除
@shared_task
def delete_guest_accounts_delayed(room_uuid:UUID) -> NoReturn:
	# ここでWebSocketの送信が完了するまで待ちたい
	time.sleep(5)
	print(f"Room<{room_uuid}> has been closed.(delayed task)")
	room_members = find_customuser_object(True, joined_room=room_uuid, is_guest=True)
	if room_members is not None:
		room_members.delete()