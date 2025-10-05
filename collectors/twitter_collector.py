# collectors/twitter_collector.py
import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

TWITTER_BEARER = os.getenv("TWITTER_BEARER")

client = tweepy.Client(bearer_token=TWITTER_BEARER)

def fetch_twitter(query="OSINT", limit=10):
    results = []
    for tweet in tweepy.Paginator(
        client.search_recent_tweets, 
        query=query, 
        tweet_fields=["author_id","created_at"], 
        max_results=50
    ).flatten(limit=limit):
        results.append({
            "platform": "Twitter",
            "user": str(tweet.author_id),
            "timestamp": str(tweet.created_at),
            "text": tweet.text,
            "url": f"https://twitter.com/i/web/status/{tweet.id}"
        })
    return results
