from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from ..forms import CustomUserLoginFrom


# ログイン画面
class CustomLoginView(LoginView):
    form_class = CustomUserLoginFrom
    redirect_authenticated_user = False
    next_page = reverse_lazy('accounts:room-settings')
    template_name = 'registration/login.html'