from apscheduler.schedulers.background import BackgroundScheduler



def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodic_task, 'interval', minutes=10)
    scheduler.start()

# APSSchedulerで定期実行
def periodic_task():
    delete_guest_accounts()    

# 期限切れのセッションの削除
def delete_guest_accounts():
    # 未実装
    pass