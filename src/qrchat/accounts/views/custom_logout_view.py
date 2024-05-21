from django.contrib.auth import logout
from django.shortcuts import redirect


# ログアウト画面
def custom_logout_view(request):
    model_object = request.user
    # ゲストはログアウト時にアカウント削除
    logout(request)
    if model_object.is_guest:
        model_object.delete()
    return redirect('accounts:custom_login')