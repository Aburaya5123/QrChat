from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
import os

from qrchat.utils.model_helper import *


# チャット画面
class ChatRoom(LoginRequiredMixin, TemplateView):
    if os.environ.get("REMOTE_DEPLOY", False):
        template_name = 'chat/chatroom_remote.html'
    else:
        template_name = 'chat/chatroom_local.html'

    def get(self, request, room_id):
        # URLからroom_idを取得
        self.room_uuid = str_to_uuid(str(room_id))
        if self.room_uuid is None:
            messages.error(self.request, '無効なURLです。')
            return redirect('accounts:custom_login')
        
        room_object = find_room_object(True, room_id=self.room_uuid)
        if room_object is None:
            messages.error(self.request, 'ルームが見つかりませんでした。')
            return redirect('accounts:custom_login')
        
        m_context = {
            'room_id':self.room_uuid,
            'room_name':room_object.first().room,
        }
        return render(request, self.template_name, context=m_context)