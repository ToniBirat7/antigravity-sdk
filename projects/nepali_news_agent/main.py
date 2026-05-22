"""
Nepali News ReACT Agent

ReACT agentic loop: fetches Nepali news from the last 60 minutes
across multiple RSS sources and delivers a clean digest.

Run: uv run python projects/nepali_news_agent/main.py
"""

import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks import policy

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from projects.nepali_news_agent.tools import (
    fetch_latest_news,
    fetch_article_content,
    list_news_sources,
    get_current_time,
)

load_dotenv(Path(__file__).parent.parent.parent / ".env")


SYSTEM_PROMPT = """You are a Nepali News Reporter Agent.

Your job each run:
1. Call get_current_time to know the current time
2. Call fetch_latest_news(cutoff_minutes=60) to get all articles from the last hour
3. For each significant article, call fetch_article_content(url) to get the full text
4. Summarize and present a concise markdown digest

Output format (strict markdown):

# 🇳🇵 Nepal News Digest — Last Hour
*{Nepal time}*

---

## {Source Name}

### {Article Headline}
> {2-3 sentence summary of what the article says — factual, no embellishment}
🕐 {N} minutes ago · [Read more]({url})

---

## Summary
- **Total articles:** {N} across {M} sources
- **Top themes:** bullet list of 3-5 recurring topics across all articles

Rules:
- Summarize only what fetch_article_content returns — never fabricate
- If article content fetch fails, write summary as "Full text unavailable" and skip summary
- Skip sources with no articles in the last hour
- Keep each article summary to 2-3 sentences max
- Use bold for key names/places/numbers in summaries"""


async def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set in .env")
        sys.exit(1)

    config = LocalAgentConfig(
        system_instructions=SYSTEM_PROMPT,
        tools=[
            get_current_time,
            list_news_sources,
            fetch_latest_news,
            fetch_article_content,
        ],
        # Allow tools to run without interactive confirmation
        policies=[policy.allow_all()],
        # No filesystem access needed — our tools handle HTTP
        capabilities=__import__(
            "google.antigravity.types", fromlist=["CapabilitiesConfig"]
        ).CapabilitiesConfig(enabled_tools=[]),
    )

    print("=" * 60)
    print("  🇳🇵 Nepali News ReACT Agent")
    print("  Fetching & summarizing news from the last 60 minutes...")
    print("=" * 60)
    print()

    async with Agent(config) as agent:
        response = await agent.chat(
            "Fetch and present the Nepal news digest for the last 60 minutes."
        )
        print(await response.text())

    print()
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
