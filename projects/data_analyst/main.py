"""
Data Analyst Agent
Demonstrates stateful multi-turn conversation for data analysis.
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig


async def main():
    load_dotenv("../../.env")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set in .env")
        return

    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Create sample data if none exists
    sample_file = data_dir / "sample.csv"
    if not sample_file.exists():
        sample_file.write_text(
            "product,sales,region,quarter\n"
            "Laptop,15000,North,Q1\n"
            "Laptop,16500,North,Q2\n"
            "Mouse,2300,East,Q1\n"
            "Mouse,2150,East,Q2\n"
            "Monitor,8900,South,Q1\n"
            "Monitor,9200,South,Q2\n"
            "Keyboard,3450,West,Q1\n"
            "Keyboard,3670,West,Q2\n"
        )
        print("Created sample data file: data/sample.csv")

    config = LocalAgentConfig(
        system_instructions=(
            "You are an expert data analyst. Your task is to help analyze CSV files, "
            "identify trends, generate insights, and answer questions about the data. "
            "Always ask clarifying questions and provide actionable recommendations. "
            "Be precise with numbers and explain your analysis clearly."
        )
    )

    print("=" * 70)
    print("DATA ANALYST AGENT")
    print("=" * 70)
    print("\nInitializing agent...\n")

    async with Agent(config) as agent:
        print("Agent ready. Starting analysis...\n")

        # Turn 1: Discover what data is available
        print("Exploring available data files...\n")
        response = await agent.chat(
            "Look at the 'data' directory in my project. What CSV files do you find? "
            "List them with brief descriptions of what they might contain."
        )
        print(await response.text())

        print("\n" + "-" * 70 + "\n")

        # Turn 2: Analyze the sample data
        print("Analyzing sample.csv...\n")
        response = await agent.chat(
            "Now read the file 'data/sample.csv' and give me a comprehensive analysis. "
            "Include: (1) table structure, (2) data types, (3) key statistics, (4) interesting patterns."
        )
        print(await response.text())

        print("\n" + "-" * 70 + "\n")

        # Turn 3: Generate insights (stateful - uses context from previous turns)
        print("Generating insights...\n")
        response = await agent.chat(
            "Based on your analysis, what are the top 3 business insights? "
            "What region performed best? What product had the highest growth?"
        )
        print(await response.text())

        print("\n" + "-" * 70 + "\n")

        # Turn 4: Recommendations (leverages multi-turn state)
        print("Recommendations...\n")
        response = await agent.chat(
            "What would you recommend to improve sales based on these insights? "
            "Should we focus on any particular region or product?"
        )
        print(await response.text())

        print("\n" + "=" * 70)
        print("Analysis complete.")
        print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
