from django.contrib.auth import logout
from django.shortcuts import redirect


# ログアウト処理
def custom_logout_view(request):
    this_user = request.user
    # ゲストはログアウト時にアカウント削除
    logout(request)
    if this_user.is_guest:
        this_user.delete()
    return redirect('accounts:custom_login')