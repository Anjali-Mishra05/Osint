import discord
import asyncio
import os
from datetime import datetime

messages = []

DISCORD_KEY = os.getenv("DISCORD_KEY")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def fetch_discord_messages(channel_id=None, timeout=10):
    """
    Fetch messages from Discord.
    - channel_id: str, optional. Agar nahi diya to server ke sabhi accessible channels se.
    - timeout: int, seconds to wait before closing.
    """
    @client.event
    async def on_ready():
        print(f"Logged in as {client.user}")
        await asyncio.sleep(timeout)
        await client.close()

    @client.event
    async def on_message(message):
        if message.author.bot:
            return
        if channel_id and str(message.channel.id) != str(channel_id):
            return
        messages.append({
            "platform": "discord",
            "user": str(message.author),
            "timestamp": str(message.created_at),
            "text": message.content,
            "url": f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
        })

    try:
        await client.start(DISCORD_KEY)
    except discord.errors.LoginFailure:
        print("Discord token invalid!")
        return []
    except Exception as e:
        print("Error fetching Discord:", e)
        return []

    return messages


if __name__ == "__main__":
    # Example: fetch from specific channel
    channel_id = None  # yaha Discord channel ID daalein agar chahiye
    data = asyncio.run(fetch_discord_messages(channel_id=channel_id))
    print(f"Fetched {len(data)} messages")
    for msg in data:
        print(msg)
