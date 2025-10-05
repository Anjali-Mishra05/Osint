import requests

def fetch_reddit(query="technology", limit=10):
    url = f"https://www.reddit.com/search.json?q={query}&limit={limit}"
    headers = {"User-agent": "OSINT-Bot"}
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        posts = resp.json().get("data", {}).get("children", [])
        results = []
        for p in posts:
            data = p.get("data", {})
            results.append({
                "user": data.get("author"),
                "text": data.get("title"),
                "url": f"https://reddit.com{data.get('permalink')}",
                "timestamp": data.get("created_utc")
            })
        return results
    except Exception as e:
        print(f"Reddit fetch error: {e}")
        return []
