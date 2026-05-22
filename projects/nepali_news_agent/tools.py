"""
Custom tools for the Nepali News Agent.

Each function is a tool the ReACT agent can call.
All tools return plain strings so the agent can reason over them.
"""

import feedparser
import httpx
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from typing import Optional


# Nepali news RSS feeds (English + Nepali)
NEWS_SOURCES = {
    "Kathmandu Post":   "https://kathmandupost.com/rss",
    "OnlineKhabar":     "https://www.onlinekhabar.com/feed",
    "My Republica":     "https://myrepublica.nagariknetwork.com/feed",
    "Ratopati":         "https://ratopati.com/rss",
    "Setopati":         "https://www.setopati.com/feed",
    "Nepal News":       "https://nepalnews.com/feed/",
    "Nagarik News":     "https://nagariknews.nagariknetwork.com/feed",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


def _parse_entry_time(entry) -> Optional[datetime]:
    """Parse entry published time to UTC-aware datetime."""
    for attr in ("published", "updated"):
        raw = getattr(entry, attr, None)
        if raw:
            try:
                return parsedate_to_datetime(raw).astimezone(timezone.utc)
            except Exception:
                pass
    # Try parsed struct
    for attr in ("published_parsed", "updated_parsed"):
        t = getattr(entry, attr, None)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return None


def fetch_latest_news(cutoff_minutes: int = 60) -> str:
    """
    Fetch news articles published in the last `cutoff_minutes` minutes
    from all Nepali news RSS sources.

    Returns a formatted string with headlines, source, time, and URL.
    """
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(minutes=cutoff_minutes)
    results = []

    for source_name, feed_url in NEWS_SOURCES.items():
        try:
            resp = httpx.get(feed_url, headers=HEADERS, timeout=10, follow_redirects=True)
            feed = feedparser.parse(resp.text)
        except Exception as e:
            results.append(f"[{source_name}] ERROR fetching feed: {e}")
            continue

        count = 0
        for entry in feed.entries:
            pub_time = _parse_entry_time(entry)
            if pub_time is None:
                # No timestamp — skip (can't verify recency)
                continue
            if pub_time < cutoff:
                continue

            title = entry.get("title", "No title").strip()
            link = entry.get("link", "").strip()
            age_mins = int((now - pub_time).total_seconds() / 60)
            results.append(
                f"[{source_name}] ({age_mins}m ago) {title}\n  URL: {link}"
            )
            count += 1

        if count == 0:
            results.append(f"[{source_name}] No articles in last {cutoff_minutes} minutes.")

    if not results:
        return f"No news found in the last {cutoff_minutes} minutes from any source."

    header = f"=== Nepali News — Last {cutoff_minutes} minutes (as of {now.strftime('%Y-%m-%d %H:%M UTC')}) ===\n"
    return header + "\n".join(results)


def fetch_article_content(url: str) -> str:
    """
    Fetch and extract the main text content of a news article URL.
    Returns cleaned article text (first ~1500 chars).
    """
    try:
        resp = httpx.get(url, headers=HEADERS, timeout=10, follow_redirects=True)
        soup = BeautifulSoup(resp.text, "lxml")

        # Remove nav, ads, scripts
        for tag in soup(["script", "style", "nav", "header", "footer", "aside", "iframe"]):
            tag.decompose()

        # Try common article body selectors
        body = None
        for selector in ["article", ".article-body", ".post-content", ".entry-content", "main"]:
            body = soup.select_one(selector)
            if body:
                break
        if body is None:
            body = soup.find("body")

        text = body.get_text(separator="\n", strip=True) if body else ""
        # Trim to 1500 chars to keep context manageable
        return text[:1500] + ("..." if len(text) > 1500 else "")
    except Exception as e:
        return f"ERROR fetching article: {e}"


def list_news_sources() -> str:
    """List all available Nepali news sources with their RSS feed URLs."""
    lines = ["Available Nepali news sources:"]
    for name, url in NEWS_SOURCES.items():
        lines.append(f"  - {name}: {url}")
    return "\n".join(lines)


def get_current_time() -> str:
    """Return current UTC time and Nepal time (UTC+5:45)."""
    utc = datetime.now(timezone.utc)
    nepal_tz = timezone(timedelta(hours=5, minutes=45))
    nepal = utc.astimezone(nepal_tz)
    return (
        f"Current time:\n"
        f"  UTC:   {utc.strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
        f"  Nepal: {nepal.strftime('%Y-%m-%d %H:%M:%S NPT')} (UTC+5:45)"
    )
