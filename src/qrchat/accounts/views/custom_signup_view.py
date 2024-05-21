from django.views.generic import CreateView
from django.contrib.auth import login
from django.shortcuts import redirect
from logging import getLogger
from django.contrib import messages

from ..forms import CustomUserCreationForm


logger = getLogger(__name__)


# 新規登録画面
class CustomSignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        try:
            form.save()
        except Exception as e:
            logger.warn(e)
            messages.error(self.request, 'アカウントの作成に失敗しました。')
            return redirect("accounts:custom_signup")

        login(self.request, form.get_user_model())

        return redirect('accounts:room-settings')