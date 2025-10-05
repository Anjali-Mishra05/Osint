import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

def plot_sentiment_pie(db_path="db/osint_data.db"):
    # Load data from DB
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM osint_data", conn)
    conn.close()

    # Compute sentiment polarity
    df["sentiment"] = df["text"].apply(lambda x: TextBlob(x).sentiment.polarity)

    # Classify sentiment
    def classify_sentiment(s):
        if s > 0.05:
            return "Positive"
        elif s < -0.05:
            return "Negative"
        else:
            return "Neutral"

    df["sentiment_label"] = df["sentiment"].apply(classify_sentiment)

    # Count each sentiment type
    counts = df["sentiment_label"].value_counts()

    # Plot pie chart
    plt.figure(figsize=(6,6))
    plt.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=["#4caf50", "#ffc107", "#f44336"],  # green, yellow, red
        startangle=90,
        explode=[0.05]*len(counts)
    )
    plt.title("Sentiment Distribution (Positive / Neutral / Negative)")
    plt.tight_layout()
    plt.show()

# Usage
plot_sentiment_pie()
