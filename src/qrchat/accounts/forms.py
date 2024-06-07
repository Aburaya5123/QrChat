from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import CustomUser
from qrchat.utils.model_helper import create_customuser_object


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('login_id',)


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('login_id',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Errorメッセージの上書き
        self.fields['login_id'].error_messages.update({
            'required': _('ログインIDを入力してください。'),
            'unique':_('このログインIDは既に使用されています。'),
            'invalid': _('ログインIDは6～30文字の間で入力してください。'),
            'max_length':_('ログインIDは30文字以内で入力してください。'),
            'min_length':_('ログインIDは6文字以上で入力してください。')
        })
        self.fields['password1'].error_messages.update({
            'required': _('パスワードを入力してください。'),
            'invalid': _('パスワードは6文字以上で入力してください。'),
            #'min_length':_('パスワードは6文字以上で入力してください。')
        })
        self.fields['password2'].error_messages.update({
            'required': _('確認用パスワードを入力してください。'),
            'invalid': _('確認用パスワードは6文字以上で入力してください。'),
            #'min_length':_('確認用パスワードは6文字以上で入力してください。'),
        })

    def clean(self):
        self.login_id = self.cleaned_data.get("login_id")
        self.password = self.cleaned_data.get("password1")
        self.password_confirm = self.cleaned_data.get("password2")
        #if self.password!=self.password_confirm:
           #self._update_errors({'password2':['入力されたパスワードが一致しません。']})
        super(CustomUserCreationForm, self).clean()
        return self.cleaned_data
    
    def save(self):
        # モデルの作成
        self.u_instance = create_customuser_object(self.login_id, self.password)
        if self.u_instance is None:
            raise Exception('Failed to create the user model.')
        
    def get_user_model(self):
        return self.u_instance


class CustomUserLoginFrom(AuthenticationForm):
    def __init__(self, request=None, **kwargs):
        super(CustomUserLoginFrom, self).__init__(request, **kwargs)
        self.username_field = 'login_id' 
        # Errorメッセージの上書き
        self.fields['username'].error_messages.update({
            'required': _('ログインIDを入力してください。'),
            'invalid': _('ログインIDに使用できない文字が含まれています。'),
        })
        self.fields['password'].error_messages.update({
            'required': _('パスワードを入力してください。'),
            'invalid': _('パスワードに使用できない文字が含まれています。'),
        })

    def clean(self):
        login_id = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if login_id is None or login_id == "" \
            or password is None or password == "":
            raise forms.ValidationError('')

        user = authenticate(self.request, login_id=login_id, password=password)
        if user is None:
            raise forms.ValidationError('ユーザーが存在しません。')
        if not user.is_active:
            raise forms.ValidationError('このアカウントはご利用いただけません。')
        
        self.user_cache = user
        super(CustomUserLoginFrom, self).clean()
        return self.cleaned_data