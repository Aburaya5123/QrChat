from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display=('username', 'user_id', 'login_id', 'joined_room', 'last_login')
    list_filter=('is_active', 'is_superuser', 'is_staff', 'is_guest')

admin.site.register(CustomUser, CustomUserAdmin)