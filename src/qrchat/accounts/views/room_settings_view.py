from django.shortcuts import redirect, render
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from logging import getLogger

from chat.forms import RoomSettingsForm
from qrchat.utils.model_helper import find_room_object


logger = getLogger(__name__)


# ルーム名設定画面
class RoomSettingsView(LoginRequiredMixin, FormView):
    form_class = RoomSettingsForm
    template_name = 'registration/roomsettings.html'

    # formからuserを参照するため、引数を追加
    def get_form_kwargs(self):
        kwargs = super(RoomSettingsView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # formに初期値を挿入
    def get(self, request):
        old_room = find_room_object(True, owner=request.user.user_id)
        if old_room is not None:
            # 前回に使用したルーム名を入力
            initial_dict = dict(room=old_room.first().room)
            m_form = RoomSettingsForm(request.GET or None, initial=initial_dict)
        else:
            m_form = RoomSettingsForm(request.GET or None)
        m_context = {'form':m_form}

        return render(request, self.template_name, context=m_context)
    
    def form_valid(self, form):
        room_name = form.cleaned_data.get('room')

        old_room = find_room_object(True, owner=self.request.user.user_id)
        # ルームの引継ぎを行う
        if old_room is not None and old_room.first().room == room_name:
            # 有効期限を再設定
            old_room.first().set_expire_date()
            old_room.first().save()
            return redirect(f"/chat/lobby/{old_room.first().room_id}/")
               
        # ルームの新規作成を行い古いルームは削除 
        #   -> accounts.signals.pyのリスナーでdeleteをキャッチ
        elif old_room is not None:
            old_room.delete()

        # 新規ルーム作成
        try:
            form.save()
            return redirect(f"/chat/lobby/{form.get_new_room_id()}/")
        except Exception as e:
            logger.error(e)
            messages.error(self.request, 'ルームの作成に失敗しました。')
            return redirect("accounts:room-settings")