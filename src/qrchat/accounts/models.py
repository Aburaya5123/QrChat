from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin)
from random import randint
from django.utils.translation import gettext_lazy as _
from uuid import uuid4


MAX_USERNAME_LENGTH = 30
MAX_LOGIN_ID_LENGTH = 30

class UserManager(BaseUserManager):

    def _create_user(self, login_id, password, icon, **extra_fields):
        user_id = uuid4()
        user = self.model(user_id=user_id, 
                          login_id=login_id, 
                          user_icon = icon,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, login_id, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_guest', False)
        return self._create_user(
            login_id=login_id,
            password=password,
            icon='♔',
            **extra_fields,
        )

    def create_superuser(self, login_id, password, **extra_fields):
        extra_fields['is_active'] = True
        extra_fields['is_superuser'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_guest'] = False
        return self._create_user(
            login_id=login_id,
            password=password,
            icon='♚',
            **extra_fields,
        )
    
    def create_guestuser(self, username=None, joined_room=None, **extra_fields):
        extra_fields['is_active'] = True
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        extra_fields['is_guest'] = True
        extra_fields['username'] = username
        extra_fields['joined_room'] = joined_room
        return self._create_user(
            login_id=str(uuid4()),
            password="guestpassword",
            icon=self.get_user_icon(),
            **extra_fields,
        )
    
    def get_user_icon(self) -> str:
        icons = ['♕', '♖', '♗', '♘', '♙', '♛', '♜', '♝', '♞']
        return icons[randint(0, len(icons)-1)]    


class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid4)
    username = models.CharField(verbose_name=_("ユーザー名"), default=None, unique=False, blank=True, null=True,
                        max_length=MAX_USERNAME_LENGTH)
    login_id = models.CharField(verbose_name=_("ログインID"), unique=True, blank=False, null=False,
                        validators=[MinLengthValidator(6)], max_length=MAX_LOGIN_ID_LENGTH)
    last_login = models.DateTimeField(auto_now=True)
    joined_room = models.UUIDField(default=None, null=True)
    is_superuser = models.BooleanField(verbose_name=_('管理者'), default=False)
    is_staff = models.BooleanField(verbose_name=_('スタッフ'), default=False)
    is_active = models.BooleanField(verbose_name=_('アクティブ'), default=True)
    is_guest = models.BooleanField(verbose_name=_('ゲスト'), default=False)
    user_icon = models.CharField(unique=False, blank=False, null=False, max_length=10)

    objects = UserManager()

    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return str(self.user_id)