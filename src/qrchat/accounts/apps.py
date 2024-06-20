from django.apps import AppConfig
import os

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # アプリの起動時に実行
        start_scheduler()
        start_signals()
    
def start_scheduler():
    # スケジューラの起動
    from .update import start
    start()

def start_signals():
    # signalsの読み込み
    import qrchat.signals