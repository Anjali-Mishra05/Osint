

import requests
import os

INSTAGRAM_USERNAME = os.getenv("********")
INSTAGRAM_PASSWORD = os.getenv("********")

def fetch_instagram():
    """
    Fetch posts from Instagram by scraping / API.
    Returns a list of dicts with keys: user, text, timestamp, url.
    """
    try:
        session = requests.Session()
        # Login (if credentials provided)
        if INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD:
            login_url = "https://www.instagram.com/accounts/login/ajax/"
            session.headers.update({
                "User-Agent": "Mozilla/5.0",
            })
            login_data = {
                "username": INSTAGRAM_USERNAME,
                "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:&:{INSTAGRAM_PASSWORD}"
            }
            login_resp = session.post(login_url, data=login_data)
            if login_resp.status_code != 200 or not login_resp.json().get("authenticated"):
                print("⚠️ Instagram login failed")

        # Example: fetch a user profile
        profile_url = f"https://www.instagram.com/{INSTAGRAM_USERNAME}/?__a=1"
        resp = session.get(profile_url)
        if resp.status_code != 200:
            print(f"❌ Instagram fetch error: {resp.status_code}")
            return []

        user_data = resp.json()
        posts = []
        for edge in user_data.get("graphql", {}).get("user", {}).get("edge_owner_to_timeline_media", {}).get("edges", []):
            node = edge.get("node")
            posts.append({
                "user": INSTAGRAM_USERNAME,
                "text": node.get("edge_media_to_caption", {}).get("edges", [{}])[0].get("node", {}).get("text", ""),
                "timestamp": node.get("taken_at_timestamp"),
                "url": f"https://instagram.com/p/{node.get('shortcode')}"
            })
        return posts

    except Exception as e:
        print(f"❌ Instagram fetch exception: {e}")
        return []
