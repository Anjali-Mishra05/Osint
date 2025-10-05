import re
from langdetect import detect

def clean_text(text):
    """Remove URLs and special characters"""
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(r"[^A-Za-z0-9\s]", "", text)  # remove symbols
    return text.strip()

def filter_english(records):
    """Keep only English-language posts"""
    filtered = []
    for r in records:
        try:
            if r.get("text") and detect(r["text"]) == "en":
                filtered.append(r)
        except:
            continue
    return filtered
