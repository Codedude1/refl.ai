import os
import requests
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def send_daily_summary():
    r = requests.get(f"{API_BASE}/summary/daily")
    if not r.ok:
        print("Failed to fetch daily summary:", r.text)
        return
    data = r.json()

    since = data["since"].split("T")[0]
    lines = ["f📊 Daily summary for {since}"]
    for cat, count in data["counts_by_type"].items():
        lines.append(f"• {cat.capitalize()}: {count}")
    lines.append(f"Total entries: {data['total_entries']}")

    message = "\n".join(lines)

    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    resp = requests.post(telegram_url, json=payload)
    if not resp.ok:
        print("Failed to send Telegram message:", resp.text)

def send_weekly_summary():
    r = requests.get(f"{API_BASE}/summary/weekly")
    if not r.ok:
        print("Failed to fetch weekly summary:", r.text)
        return
    data = r.json()

    since = data["since"].split("T")[0]
    lines = ["f📊 Weekly summary for {since}"]
    for cat, count in data["counts_by_type"].items():
        lines.append(f"• {cat.capitalize()}: {count}")
    lines.append(f"Total entries: {data['total_entries']}")

    message = "\n".join(lines)

    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    resp = requests.post(telegram_url, json=payload)
    if not resp.ok:
        print("Failed to send Telegram message:", resp.text)

def send_monthly_summary():
    r = requests.get(f"{API_BASE}/summary/monthly")
    if not r.ok:
        print("Failed to fetch monthly summary:", r.text)
        return
    data = r.json()

    since = data["since"].split("T")[0]
    lines = ["f📊 Monthly summary for {since}"]
    for cat, count in data["counts_by_type"].items():
        lines.append(f"• {cat.capitalize()}: {count}")
    lines.append(f"Total entries: {data['total_entries']}")

    message = "\n".join(lines)

    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    resp = requests.post(telegram_url, json=payload)
    if not resp.ok:
        print("Failed to send Telegram message:", resp.text)


scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")

scheduler.add_job(send_daily_summary, "cron", hour = 21, minute = 0) 

scheduler.add_job(send_weekly_summary, "cron", day_of_week="sun", hour=21, minute=0)

scheduler.add_job(send_monthly_summary, "cron", day=30, hour=21, minute=0)

def start_scheduler():
    """Call this once your event loop is running."""
    scheduler.start()
