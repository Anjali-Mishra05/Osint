import snscrape.modules.twitter as sntwitter

def fetch_twitter(query="OSINT", limit=10):
    """
    Scrape Twitter posts without API keys using snscrape.
    Returns a list of dicts with user, text, timestamp, and url.
    """
    results = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= limit:
            break
        results.append({
            "user": tweet.user.username,
            "text": tweet.content,
            "timestamp": str(tweet.date),
            "url": tweet.url
        })
    return results
