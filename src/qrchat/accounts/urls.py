from django.urls import path, re_path
from django.views.generic import RedirectView

from .views import custom_login_view, custom_logout_view, custom_signup_view, room_settings_view

app_name = 'accounts'

urlpatterns = [
    path('signup/', custom_signup_view.CustomSignUpView.as_view(), name='custom_signup'),
    path("login/", custom_login_view.CustomLoginView.as_view(), name="custom_login"),
    path("logout/", custom_logout_view.custom_logout_view, name="custom_logout"),
    path("room-settings/", room_settings_view.RoomSettingsView.as_view(), name="room-settings"),
    re_path(r'.*', RedirectView.as_view(url='/accounts/login/')),
]