import asyncio
import pandas as pd
from pathlib import Path
import sqlite3
from tabulate import tabulate
from dotenv import load_dotenv
import schedule
import time
from datetime import datetime
import os
import matplotlib.pyplot as plt

from collectors.twitter_collector import fetch_twitter
from collectors.discord_collector import fetch_discord_messages
from collectors.github_collector import fetch_github
from collectors.telegram_collector import fetch_telegram
from collectors.instagram_collector import fetch_instagram
from collectors.reddit_collector import fetch_reddit

from utils.cleaner import clean_text, filter_english
from utils.sentiment import add_sentiment
from utils.database import save_to_db, check_duplicate

load_dotenv()

DB_PATH = Path(__file__).parent / "db" / "osint_data.db"
TABLE_NAME = "social_media_posts"
CSV_PATH = Path(__file__).parent / "osint_data.csv"


# ---------------- Helpers ----------------
def normalize_record(item, platform):
    if not item:
        return None

    user = item.get("user") or item.get("username") or "N/A"
    timestamp = item.get("timestamp") or item.get("date") or item.get("created_at") or datetime.utcnow().isoformat()
    text = item.get("text") or item.get("caption") or item.get("description") or "No text"
    url = item.get("url") or item.get("link") or ""

    if platform == "Telegram":
        if isinstance(item, dict):
            user = item.get("user") or item.get("username") or "TelegramUser"
            text = item.get("text") or "No text"
            timestamp = item.get("timestamp") or datetime.utcnow().isoformat()
            url = f"https://t.me/{user}" if user != "N/A" else ""
        else:
            user = "TelegramUser"
            text = str(item)
            timestamp = datetime.utcnow().isoformat()
            url = ""

    text = text.replace("\n", " ")

    return {
        "platform": platform,
        "user": user,
        "timestamp": timestamp,
        "text": text,
        "url": url,
        "sentiment": None
    }


def print_db_summary(data, limit=10):
    if not data:
        print("⚠️ No records to display")
        return

    print(f"\n📄 Showing first {min(limit, len(data))} records:")
    table_data = []
    for d in data[:limit]:
        table_data.append([
            d['platform'],
            d['user'],
            d['timestamp'],
            d['text'][:50] + ("..." if len(d['text'])>50 else ""),
            d['url'],
            d['sentiment']
        ])
    print(tabulate(table_data, headers=["Platform","User","Timestamp","Text","URL","Sentiment"], tablefmt="fancy_grid"))


def export_csv():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
        df.to_csv(CSV_PATH, index=False)
        conn.close()
        print(f"💾 Exported data to CSV: {CSV_PATH}")
    except PermissionError:
        print(f"⚠️ Cannot write CSV, file may be open elsewhere: {CSV_PATH}")


# ---------------- Sentiment Pie Chart ----------------
def plot_sentiment_pie(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()

    # Classify sentiment
    def classify_sentiment(score):
        if score > 0:
            return "Positive"
        elif score < 0:
            return "Negative"
        else:
            return "Neutral"

    df["sentiment_label"] = df["sentiment"].apply(classify_sentiment)
    counts = df["sentiment_label"].value_counts()

    plt.figure(figsize=(6,6))
    plt.pie(counts, labels=counts.index, autopct="%1.1f%%", colors=["#4CAF50","#F44336","#FFC107"])
    plt.title("Sentiment Distribution (Positive / Negative / Neutral)")
    plt.show()


# ---------------- Main Pipeline ----------------
async def run_pipeline(total_records=100):
    data = []

    platforms = [
        ("Twitter", fetch_twitter, ("Java", 1)),
        ("Discord", fetch_discord_messages, ()),
        ("GitHub", fetch_github, ("Internships", 15)),
        ("Telegram", fetch_telegram, ()),
        ("Instagram", fetch_instagram, ()),
        ("Reddit", fetch_reddit, ("Jobs", 20))
    ]

    for platform_name, func, args in platforms:
        try:
            if platform_name == "Instagram":
                if not os.getenv("INSTAGRAM_USERNAME") or not os.getenv("INSTAGRAM_PASSWORD"):
                    print(f"⚠️ Skipping Instagram, credentials missing")
                    continue

            if asyncio.iscoroutinefunction(func):
                platform_data = await func(*args)
            else:
                platform_data = func(*args)

            if not platform_data:
                print(f"⚠️ No data returned from {platform_name}")
                continue

            normalized = [normalize_record(d, platform_name) for d in platform_data if d]
            normalized = [n for n in normalized if not check_duplicate(DB_PATH, TABLE_NAME, n)]
            data.extend(normalized)

            print(f"✅ Fetched {len(normalized)} records from {platform_name}")

        except Exception as e:
            print(f"fetching {platform_name}: {e}")

        if len(data) >= total_records:
            data = data[:total_records]
            break

    # Clean & filter
    for d in data:
        d["text"] = clean_text(d.get("text", "")).replace("\n", " ")
    data = filter_english(data)
    data = data[:total_records]

    # Add sentiment
    data = add_sentiment(data)

    # Save to DB
    save_to_db(data, DB_PATH)
    print(f"💾 Saved {len(data)} records to database")

    # Print summary
    print_db_summary(data, limit=total_records)

    # Export CSV
    export_csv()

    # Plot sentiment pie chart
    plot_sentiment_pie()


# ---------------- Scheduler ----------------
def scheduled_run():
    print("⏱️ Starting scheduled OSINT pipeline...")
    asyncio.run(run_pipeline(total_records=50))
    print("✅ Scheduled run completed.\n")


# ---------------- Run ----------------
if __name__ == "__main__":
    asyncio.run(run_pipeline(total_records=50))

    schedule.every(1).hours.do(scheduled_run)
    print("📅 Scheduler started. Press Ctrl+C to stop.")

    while True:
        schedule.run_pending()
        time.sleep(60)
