from textblob import TextBlob

def add_sentiment(records):
    """Add polarity score for sentiment analysis"""
    for r in records:
        text = r.get("text", "")
        r["sentiment"] = TextBlob(text).sentiment.polarity
    return records
