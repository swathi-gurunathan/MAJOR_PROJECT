# scheduler/job_scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from backend.agents.appointment_agent import build_appointment_agent

def send_daily_meeting_reminder():
    agent = build_appointment_agent()
    agent.run("Remind user about the 11 AM meeting")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_daily_meeting_reminder, 'cron', hour=10)
    scheduler.start()
