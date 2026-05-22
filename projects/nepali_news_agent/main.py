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
3. Present a clean, structured digest

Output format:
- Header: "🇳🇵 Nepal News Digest — Last Hour" with Nepal time
- Group articles by source
- Each article: headline, how many minutes ago, URL
- At the end: total article count across all sources
- If no articles found for a source, skip that source
- If no articles found at all, say so clearly

Be factual. Do not fabricate or embellish news content."""


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
    print("  Fetching news from the last 60 minutes...")
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
