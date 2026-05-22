"""
Example: Using custom tools with Antigravity agents.

This script demonstrates how to extend an agent with custom tool bindings.
The agent will have access to both built-in tools (file system) and custom tools.
"""

import asyncio
import os
from dotenv import load_dotenv
from google.antigravity import Agent, LocalAgentConfig


async def main():
    load_dotenv("../.env")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set in .env")
        return

    config = LocalAgentConfig(
        system_instructions=(
            "You are a helpful assistant with access to custom tools. "
            "Use them to help the user with their requests."
        )
    )

    print("Initializing agent with custom tools...\n")

    async with Agent(config) as agent:
        print("Agent initialized with custom tools.\n")

        # Note: The SDK automatically provides built-in tools like:
        # - read_file(path)
        # - write_file(path, content)
        # - list_directory(path)
        # - execute_command(cmd)
        # - navigate_directory(path)

        # Example: Use built-in file system tools
        print("Demonstrating built-in file tools:\n")
        response = await agent.chat(
            "Create a file called 'hello.txt' in the current directory "
            "with the content 'Hello from Antigravity Agent!' "
            "Then read it back and confirm the content."
        )
        print(await response.text())

        print("\n" + "-" * 60 + "\n")

        # The agent can chain multiple operations
        print("Chaining operations (multi-turn):\n")
        response = await agent.chat(
            "Now list all text files (.txt) in the current directory. "
            "For each file, read its content and tell me what it says."
        )
        print(await response.text())


if __name__ == "__main__":
    asyncio.run(main())
