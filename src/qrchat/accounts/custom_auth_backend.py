from django.contrib.auth.backends import BaseBackend

from .models import CustomUser

        
class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, login_id=None, password=None, username=None, **kwargs):
        try:
            if login_id is None:
                user = CustomUser.objects.get(login_id=username)
            else:
                user = CustomUser.objects.get(login_id=login_id)
        except CustomUser.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
    
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None