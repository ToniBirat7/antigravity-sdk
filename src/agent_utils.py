"""
Utility functions for working with Antigravity agents.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


def load_env(env_path: str = ".env") -> bool:
    """
    Load environment variables from .env file.
    Returns True if API key is available, False otherwise.
    """
    load_dotenv(env_path)
    api_key = os.getenv("GEMINI_API_KEY")
    return bool(api_key)


def ensure_data_dir(path: str = "data") -> Path:
    """
    Ensure a data directory exists.
    Returns the Path object.
    """
    data_dir = Path(path)
    data_dir.mkdir(exist_ok=True)
    return data_dir


def create_sample_csv(file_path: str, data: str) -> Path:
    """
    Create a sample CSV file if it doesn't exist.
    Returns the Path object.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(data)
    return path


def format_response(title: str, content: str) -> str:
    """
    Format agent response with title and separator.
    """
    separator = "=" * 70
    return f"\n{separator}\n{title}\n{separator}\n{content}\n"
