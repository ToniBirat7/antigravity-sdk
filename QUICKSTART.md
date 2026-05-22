# Quick Start Guide

Get up and running with the Antigravity SDK in 3 steps.

## 1. Set Your API Key

```bash
# Copy the example and add your key
cp .env.example .env

# Edit .env and paste your Gemini API key
# Get one at: https://aistudio.google.com/app/apikey
```

## 2. Run a Test Script

```bash
# Try the basic example (requires API key to be set)
python examples/basic_test.py
```

You should see the agent explore your project structure and provide insights.

## 3. Run the Data Analyst Project

```bash
cd projects/data_analyst
python main.py
```

This demonstrates:
- Multi-turn stateful conversation
- File system access (reading CSV files)
- Data analysis and insights generation
- Context preservation across agent.chat() calls

## What You'll Learn

| Script | Demonstrates |
|--------|--------------|
| `examples/basic_test.py` | Core concepts: async context, multi-turn chat, context preservation |
| `examples/custom_tools.py` | Built-in file system tools (read, write, execute) |
| `projects/data_analyst/main.py` | Real-world workflow: load → analyze → recommend |

## Next Steps

1. **Modify examples**: Change the prompts in `basic_test.py` to ask different questions
2. **Create your own project**: Copy `projects/data_analyst/` and build something new
3. **Explore the SDK**: Check what other tools/capabilities are available
4. **Build a tool binding**: Extend agents with custom tools for your use case

## Troubleshooting

**"GEMINI_API_KEY not set"**
- Ensure `.env` file exists in the project root with your API key

**"Module not found"**
- Run `uv sync` to ensure dependencies are installed

**Agent seems slow**
- First API call takes time as it initializes. Subsequent calls are faster.
- Check your internet connection and API quota.

## Project Structure Reference

```
.
├── examples/           # Runnable scripts to learn the SDK
├── projects/
│   └── data_analyst/   # Full example project (ready to run)
├── src/                # Reusable utilities and helpers
├── tests/              # Test suite (coming soon)
├── .env.example        # Template for environment config
├── CLAUDE.md           # Full documentation
├── pyproject.toml      # Project dependencies (managed by uv)
└── QUICKSTART.md       # This file
```

## Tips for Learning

- **Start simple**: Run `basic_test.py` first
- **Read the code**: Comments explain what's happening
- **Experiment**: Modify prompts and observe behavior
- **Check response.text()**: This is where the agent's output is
- **Use print statements**: Debug what the agent is doing
