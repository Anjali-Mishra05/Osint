# collectors/telegram_collector.py

import aiohttp
import asyncio
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def fetch_telegram():
    """
    Fetch latest messages from a Telegram channel using Bot API.
    Returns a list of dicts with keys: user, text, timestamp, url.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram credentials missing")
        return []

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    print(f"❌ Telegram API error: {resp.status}")
                    return []
                data = await resp.json()

        messages = []
        for update in data.get("result", []):
            msg = update.get("message")
            if not msg:
                continue
            messages.append({
                "user": msg.get("from", {}).get("username", "N/A"),
                "text": msg.get("text", ""),
                "timestamp": msg.get("date", "N/A"),
                "url": f"https://t.me/{msg.get('from', {}).get('username', '')}" if msg.get("from") else ""
            })
        return messages

    except Exception as e:
        print(f"❌ Telegram fetch exception: {e}")
        return []
