import requests

def fetch_github(query="machine learning", limit=10):
    url = f"https://api.github.com/search/repositories?q={query}&sort=updated&order=desc"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        items = resp.json().get("items", [])[:limit]
        results = []
        for repo in items:
            results.append({
                "user": repo.get("owner", {}).get("login"),
                "text": repo.get("description"),
                "url": repo.get("html_url"),
                "timestamp": repo.get("updated_at")
            })
        return results
    except Exception as e:
        print(f"GitHub fetch error: {e}")
        return []
