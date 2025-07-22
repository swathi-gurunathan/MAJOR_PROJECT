from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

def send_reminders():
    print(f"Reminder sent at {datetime.now()}")

def get_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_reminders, 'interval', minutes=5)
    scheduler.start()
    return scheduler

# Initialize the scheduler
get_scheduler()
