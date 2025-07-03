from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot
import sqlite3, os

def send_reminders():
    conn = sqlite3.connect("users.db")
    for uid, name in conn.execute("SELECT id, name FROM users"):
        Bot(os.getenv("BOT_TOKEN")).send_message(uid, f"Привет, {name}! Пора откладывать 😉")
    conn.close()

def schedule_reminders():
    sched = BackgroundScheduler()
    sched.add_job(send_reminders, 'cron', day=1, hour=9)
    sched.start()
