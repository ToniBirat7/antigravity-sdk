"""
Basic Antigravity SDK test script.
Demonstrates the core concepts: async context, multi-turn conversation, built-in tools.
"""

import asyncio
import os
from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig


async def main():
    load_dotenv()

    # Verify API key is available
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set. Create a .env file with your API key.")
        return

    # Define agent configuration
    config = LocalAgentConfig(
        system_instructions=(
            "You are an expert Python developer and data analyst. "
            "Your role is to help explore and understand the structure of projects. "
            "Be precise, helpful, and provide actionable insights."
        )
    )

    print("Initializing Antigravity Agent...\n")

    # The async context manager handles lifecycle
    async with Agent(config) as agent:
        print("Agent initialized. Starting conversation...\n")
        print("=" * 60)

        # First turn: Explore the project structure
        print("\nQUERY 1: What's in this directory?\n")
        response = await agent.chat("List all files and folders in the current directory. Give me a brief summary.")
        print(await response.text())

        print("\n" + "=" * 60)

        # Second turn: Analyze what we found
        print("\nQUERY 2: Analyze the project structure\n")
        response = await agent.chat(
            "Based on what you see, this appears to be a practice repository for the Google Antigravity SDK. "
            "What kinds of projects or experiments would be good for someone learning this SDK?"
        )
        print(await response.text())

        print("\n" + "=" * 60)

        # Third turn: Specific task
        print("\nQUERY 3: Suggest a project\n")
        response = await agent.chat(
            "Suggest a small, concrete project that would teach me how to use the Antigravity SDK effectively. "
            "Consider: (1) file system access, (2) multi-turn state, (3) practical utility."
        )
        print(await response.text())

        print("\n" + "=" * 60)
        print("\nConversation complete. Agent session closed.\n")


if __name__ == "__main__":
    asyncio.run(main())
