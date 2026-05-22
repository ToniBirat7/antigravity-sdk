# Google Antigravity SDK Learning Lab

This repository is a practice environment for learning and experimenting with the **Google Antigravity SDK** — a framework for building autonomous agents powered by Google's Gemini API.

## Project Structure

```
.
├── projects/              # Production-like project implementations
│   ├── data_analyst/      # Example: Data analysis & visualization agent
│   └── [add more here]
├── examples/              # Quick reference scripts and prototypes
├── src/                   # Reusable utility modules
├── tests/                 # Test suite
├── .env                   # Local secrets (Git-ignored)
├── pyproject.toml         # uv project config + dependencies
└── CLAUDE.md              # This file
```

## Environment Setup

### Prerequisites
- Python 3.11+
- `uv` package manager installed
- Google API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Installation

1. **Create and activate the virtual environment:**
   ```bash
   uv sync
   ```

2. **Set your Gemini API key:**
   ```bash
   # Create a .env file in the project root
   echo 'GEMINI_API_KEY="your_api_key_here"' > .env
   ```
   The SDK automatically loads this from the environment.

## Running Projects

Each project in `projects/` has its own entrypoint:

```bash
# Example: Run the data analyst agent
cd projects/data_analyst
python main.py
```

## Key Concepts

### The Async Context Manager
The SDK's `async with Agent(config) as agent:` pattern manages binary setup, tool binding, and cleanup automatically. Never skip this pattern.

### Built-in Tools
When you initialize an agent with `LocalAgentConfig`, it automatically gets access to:
- **File system operations**: Read/write files, navigate directories
- **Code inspection**: Analyze project structure
- **Command execution**: Run shell commands in a controlled sandbox
- **More**: Extensible via tool definitions

### Multi-turn Stateful Conversations
The agent remembers context across `await agent.chat(...)` calls within the same session, enabling iterative problem-solving.

### Tool Binding
Agents can bind custom tools via the SDK's decorator pattern (see `examples/custom_tools.py` for reference).

## Example Workflow

```python
import asyncio
from google.antigravity import Agent, LocalAgentConfig
import os

async def main():
    config = LocalAgentConfig(
        system_instructions="You are a helpful developer assistant."
    )
    
    async with Agent(config) as agent:
        # Multi-turn conversation
        response = await agent.chat("List all Python files in the current directory")
        print(await response.text())
        
        response = await agent.chat("Summarize what these files do")
        print(await response.text())

if __name__ == "__main__":
    asyncio.run(main())
```

## Project Ideas for Practice

1. **Data Analyst** ✓ (included) — Parse CSV files, generate insights
2. **Code Reviewer** — Analyze code quality, suggest improvements
3. **File Organizer** — Batch rename, sort, and categorize files
4. **Documentation Generator** — Extract docstrings and create API docs
5. **Log Analyzer** — Parse logs, identify patterns and errors

## Testing & Debugging

Run tests with:
```bash
uv run pytest tests/
```

Enable SDK debugging by setting:
```bash
export DEBUG=1
```

## References

- [Google Antigravity SDK Docs](https://github.com/google/antigravity)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Async Python Guide](https://docs.python.org/3/library/asyncio.html)

## Notes for Exploration

- The SDK is designed for **autonomous agent workflows** — perfect for iterative tasks
- Statefulness means the agent learns context, reducing boilerplate
- Tools are sandboxed, so agents can safely interact with your file system
- Experiment with different `system_instructions` to customize agent behavior
