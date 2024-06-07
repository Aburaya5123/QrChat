from django import forms
from django.utils.translation import gettext_lazy as _
from uuid import UUID

from .models import Room
from qrchat.utils.model_helper import create_room_object, find_customuser_object


class RoomSettingsForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room']

    def __init__(self, *args, **kwargs):
        # viewからuserオブジェクトの受け取り
        self.u_instance = kwargs.pop('user', None)
        super(RoomSettingsForm, self).__init__(*args, **kwargs)
        self.fields['room'].error_messages.update({
            'required': _('ルーム名を入力してください。'),
            'invalid': _('ルーム名は1～30字の間で指定してください。'),
        })
    
    # room新規作成
    def save(self):
        room_name = self.cleaned_data.get('room')
        if self.u_instance is not None:
            new_room = create_room_object(room_name, self.u_instance)
            if new_room is not None:
                self.new_room_id = new_room.room_id
                return
        raise Exception("Failed to create the room object.")
    
    def get_new_room_id(self):
        return str(self.new_room_id)


class RoomUsernameForm(forms.Form):
    room_username = forms.CharField(label=_("ユーザー名"), max_length=30, min_length=1, required=True,
                                    error_messages={'required': _('ユーザー名は1文字以上で指定してください。'),
                                                    'invalid': _('ユーザー名は1～30字の間で指定してください。')})
    room_uuid = forms.UUIDField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        # viewからuserオブジェクトの受け取り
        self.u_instance = kwargs.pop('user', None)
        super(RoomUsernameForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        super(RoomUsernameForm, self).clean()
        username = self.cleaned_data.get('room_username')
        room_uuid = self.cleaned_data.get('room_uuid')
        if type(room_uuid) is not UUID:
            raise forms.ValidationError('ルームの取得に失敗しました。')
        elif username is None or username == "":
            raise forms.ValidationError('')

        # usernameの重複確認
        duplicate_uname = find_customuser_object(True, username=username, joined_room=room_uuid)

        if self.u_instance.is_authenticated and duplicate_uname is not None:
            if duplicate_uname.exclude(pk=self.u_instance.pk).exists():
                raise forms.ValidationError('既に使用されているユーザー名です。')
        else:
            if duplicate_uname is not None:
                raise forms.ValidationError('既に使用されているユーザー名です。')
        return self.cleaned_data