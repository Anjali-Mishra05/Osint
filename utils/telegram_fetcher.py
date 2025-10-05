# utils/telegram_fetcher.py
import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def fetch_telegram_messages(limit=5):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram bot token/chat id missing")
        return []

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    try:
        response = requests.get(url)
        data = response.json()

        messages = []
        for update in data.get("result", [])[-limit:]:
            msg = update.get("message", {})
            if "text" in msg:
                messages.append({
                    "platform": "Telegram",
                    "user": msg["from"]["username"] if "username" in msg["from"] else msg["from"]["first_name"],
                    "timestamp": msg["date"],
                    "text": msg["text"],
                    "url": f"https://t.me/c/{TELEGRAM_CHAT_ID}/{msg['message_id']}"
                })
        return messages
    except Exception as e:
        print("❌ Error fetching Telegram:", e)
        return []
