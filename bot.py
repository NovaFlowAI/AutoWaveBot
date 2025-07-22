import json, random, requests, os, tweepy, google.generativeai as genai

# Load config
with open("config.json") as f:
    cfg = json.load(f)

# Gemini setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Twitter client
client = tweepy.Client(
    bearer_token=os.getenv("TW_BEARER_TOKEN"),
    consumer_key=os.getenv("TW_API_KEY"),
    consumer_secret=os.getenv("TW_API_SECRET"),
    access_token=os.getenv("TW_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TW_ACCESS_SECRET")
)

def get_trending():
    """Fetch top 5 trending topics worldwide."""
    api = tweepy.API(tweepy.OAuth1UserHandler(
        os.getenv("TW_API_KEY"),
        os.getenv("TW_API_SECRET"),
        os.getenv("TW_ACCESS_TOKEN"),
        os.getenv("TW_ACCESS_SECRET")
    ))
    trends = api.get_place_trends(id=1)[0]["trends"]
    return random.choice([t["name"] for t in trends[:5]])

def generate_tweet(trend):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Write a 260-char tweet about '{trend}' with curiosity hook & emoji."
    return model.generate_content(prompt).text.strip()

def create_tweet():
    trend = get_trending()
    text = generate_tweet(trend)
    client.create_tweet(text=text)
    print("Tweet posted:", text)

if __name__ == "__main__":
    create_tweet()
  {
  "keywords": ["tech news", "AI trends", "startup tips"],
  "tweet_template": "🔥 Latest scoop: {text}\n👉 {link}",
  "link": "https://lynk.id/yourlink"
}
tweepy==4.14.0
requests==2.31.0
google-generativeai==0.3.2
name: Auto Tweet
on:
  schedule:
    - cron: "0 */6 * * *"   # every 6 h
  workflow_dispatch:        # manual run
jobs:
  tweet:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python bot.py
        env:
          TW_API_KEY: ${{ secrets.TW_API_KEY }}
          TW_API_SECRET: ${{ secrets.TW_API_SECRET }}
          TW_ACCESS_TOKEN: ${{ secrets.TW_ACCESS_TOKEN }}
          TW_ACCESS_SECRET: ${{ secrets.TW_ACCESS_SECRET }}
          TW_BEARER_TOKEN: ${{ secrets.TW_BEARER_TOKEN }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
| Name               | Value (from dev portals) |
| ------------------ | ------------------------ |
| `TW_API_KEY`       | `xxxxxxxxxxxxxxxxxx`     |
| `TW_API_SECRET`    | `xxxxxxxxxxxxxxxxxx`     |
| `TW_ACCESS_TOKEN`  | `xxxxxxxxxxxxxxxxxx`     |
| `TW_ACCESS_SECRET` | `xxxxxxxxxxxxxxxxxx`     |
| `TW_BEARER_TOKEN`  | `xxxxxxxxxxxxxxxxxx`     |
| `GEMINI_API_KEY`   | `xxxxxxxxxxxxxxxxxx`     |
