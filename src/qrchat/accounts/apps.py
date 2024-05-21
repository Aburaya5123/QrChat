from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        start_scheduler()
        start_signals()
    
def start_scheduler():
    # スケジューラの起動
    from .update import start
    start()

def start_signals():
    import qrchat.signals