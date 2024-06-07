from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib import messages
from logging import getLogger
from django.views.generic import FormView
from uuid import UUID

from qrchat.utils.model_helper import *
from ..forms import RoomUsernameForm


logger = getLogger(__name__)


# チャットルームでのユーザー名の設定画面
class ChatLobby(FormView):
    template_name = 'chat/chat_lobby.html'
    form_class = RoomUsernameForm

    # formに引数を追加
    def get_form_kwargs(self):
        kwargs = super(ChatLobby, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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
                  
        room_name = room_object.first().room
        # room_idをhidden formに入力
        initial_dict = dict(room_uuid=self.room_uuid)
        # ゲスト以外は、前回使用したユーザー名があればusername formに出力
        if request.user.is_authenticated and \
            not request.user.is_guest and \
                request.user.username is not None:
            initial_dict['room_username']=request.user.username

        m_form = RoomUsernameForm(request.GET or None, initial=initial_dict)
        context = {
            'room_name':room_name,
            'form':m_form,
            'room_qrcode':room_object.first().qrcode.url
        }
        return render(request, self.template_name, context)
    
    def form_valid(self, form):
        room_uuid = form.cleaned_data.get('room_uuid')
        if type(room_uuid) is not UUID:
            messages.error(self.request, '無効なURLです。')
            return redirect('accounts:custom_login')
        username = form.cleaned_data.get('room_username')

        # 未認証の場合は、ゲストアカウントの作成
        if not self.request.user.is_authenticated:
            guest_user = create_guestuser_object(username, room_uuid)
            if guest_user is None:
                messages.error(self.request, 'ゲストアカウントの作成に失敗しました。')
                return redirect(f"/chat/lobby/{str(room_uuid)}/")
            login(self.request, guest_user)
        else:
            # ユーザー名の更新
            if self.request.user.username != username:
                update_customuser_model({'username':username}, u_instance=self.request.user)

        return redirect(f"/chat/room/{str(room_uuid)}/")
    
    # 以降、FormValidationError時に、contextを追加する処理
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        room_uuid = request.POST.get('room_uuid')
        if type(str_to_uuid(room_uuid)) is UUID:
            self.room_uuid = room_uuid
        else:
            messages.error(request, '無効なルームIDです。')
            return redirect('accounts:custom_login')
        return super(ChatLobby, self).post(request, *args, **kwargs)
    
    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any) -> HttpResponse:
        if self.room_uuid is not None:
            room_object = find_room_object(True, room_id=self.room_uuid)
            if room_object is not None:
                context['room_qrcode'] = room_object.first().qrcode.url
                context['room_name'] = room_object.first().room
        return super().render_to_response(context, **response_kwargs)