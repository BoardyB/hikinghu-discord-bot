import json
import os
import feedparser
import requests

# === CONFIG ===
SUBREDDIT_RSS = "https://www.reddit.com/r/hikingHungary/new/.rss"
WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]  # stored as secret in Actions
STATE_FILE = "posted.json"

# Load posted links
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        posted_links = sorted(set(json.load(f)))
        print(f"posted_links size {len(posted_links)}")
else:
    posted_links = set()


headers = {"User-Agent": "Mozilla/5.0 (MyRSSBot/1.0)"}

resp = requests.get(SUBREDDIT_RSS, headers=headers)

feed = feedparser.parse(resp.text)
new_posts = []

for entry in reversed(feed.entries):  # oldest first
    print(f"Entry title: {entry.title} link: {entry.link}")
    if entry.link not in posted_links:
        new_posts.append(entry)

print(f"new_posts size {len(new_posts)}")
for entry in new_posts:
    payload = {
        "thread_name": entry.title[:90],  # Discord max ~100 chars
        "content": f"**New post on r/hikingHungary**\n{entry.link}"
    }
    r = requests.post(WEBHOOK_URL, json=payload)
    if r.status_code == 200 or r.status_code == 204:
        print(f"Posted: {entry.title}")
        posted_links.add(entry.link)
    else:
        print(f"Failed to post {entry.title}: {r.text}")

# Save updated state
with open(STATE_FILE, "w") as f:
    json.dump(list(posted_links), f, indent=2)