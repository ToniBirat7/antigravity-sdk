# Antigravity SDK Learning Lab

A structured learning environment for the Google Antigravity SDK—a framework for building autonomous agents powered by Google's Gemini API.

## Overview

This repository provides:
- **Examples**: Quick reference scripts demonstrating core SDK concepts
- **Projects**: Production-like implementations showcasing real-world workflows
- **Utilities**: Reusable modules for common agent patterns
- **Documentation**: Comprehensive guides for setup and usage

## Prerequisites

- Python 3.11 or higher
- `uv` package manager
- Google API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

## Quick Start

### 1. Setup

```bash
# Install dependencies
uv sync

# Create .env file with your API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 2. Run Examples

```bash
# Basic agent interaction
python examples/basic_test.py

# File system operations
python examples/custom_tools.py
```

### 3. Run Projects

```bash
cd projects/data_analyst
python main.py
```

## Project Structure

```
.
├── examples/              # Quick reference scripts
│   ├── basic_test.py      # Core concepts: async, multi-turn, context
│   └── custom_tools.py    # File system operations
├── projects/              # Full workflow implementations
│   └── data_analyst/      # CSV analysis and insights
├── src/                   # Reusable utilities
│   └── agent_utils.py     # Helper functions
├── tests/                 # Test suite
├── .env.example           # Environment template
├── CLAUDE.md              # Full documentation
├── QUICKSTART.md          # 3-step getting started
└── README.md              # This file
```

## Key Concepts

### Async Context Managers
The SDK's `async with Agent(config) as agent:` pattern handles initialization, tool binding, and cleanup automatically.

### Built-in Tools
Agents automatically have access to:
- File system operations (read, write, navigate)
- Code inspection and analysis
- Command execution in a sandboxed environment

### Stateful Multi-turn Conversations
Agents maintain context across `agent.chat()` calls, enabling iterative problem-solving without boilerplate.

### System Instructions
Customize agent behavior by setting detailed system instructions that define the agent's role and constraints.

## Examples

### Basic Multi-turn Conversation

```python
import asyncio
from google.antigravity import Agent, LocalAgentConfig
import os

async def main():
    os.getenv("GEMINI_API_KEY")  # Requires .env file
    
    config = LocalAgentConfig(
        system_instructions="You are a helpful developer."
    )
    
    async with Agent(config) as agent:
        response = await agent.chat("List Python files here")
        print(await response.text())
        
        response = await agent.chat("What do these files do?")
        print(await response.text())

if __name__ == "__main__":
    asyncio.run(main())
```

## Project Ideas for Practice

1. **Code Reviewer** - Analyze code quality, suggest improvements
2. **File Organizer** - Batch rename, sort, and categorize files
3. **Documentation Generator** - Extract docstrings, create API docs
4. **Log Analyzer** - Parse logs, identify patterns and errors
5. **Data Pipeline** - Process and transform data with analysis

## Troubleshooting

**"GEMINI_API_KEY not set"**
- Ensure `.env` file exists in project root with your API key

**"Module not found"**
- Run `uv sync` to install dependencies

**Agent responses are slow**
- First API call takes time for initialization
- Subsequent calls are faster
- Check your internet connection and API quota

## References

- [Google Antigravity SDK Docs](https://github.com/google/antigravity)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Async Python Guide](https://docs.python.org/3/library/asyncio.html)

## Next Steps

1. Run `examples/basic_test.py` to see a working agent
2. Modify the example prompts to experiment with agent behavior
3. Copy `projects/data_analyst/` and customize it for your use case
4. Explore the SDK documentation for advanced patterns
5. Build custom tool bindings for your specific domain

## License

This repository is a learning lab for the Google Antigravity SDK.
