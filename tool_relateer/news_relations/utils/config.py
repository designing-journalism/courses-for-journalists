"""
Configuration utilities for the news relations application.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Flask settings
FLASK_APP = os.getenv("FLASK_APP", "app.py")
FLASK_ENV = os.getenv("FLASK_ENV", "development")
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

# AI Provider settings
DEFAULT_AI_PROVIDER = os.getenv("DEFAULT_AI_PROVIDER", "ollama")

# Ollama settings
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Anthropic (Claude) settings
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")

# Vector database settings
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./vector_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# News data settings
NEWS_ITEMS_DIR = os.getenv("NEWS_ITEMS_DIR", "../news-items")

# Ensure paths are absolute
BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DB_PATH = Path(VECTOR_DB_PATH)
if not VECTOR_DB_PATH.is_absolute():
    VECTOR_DB_PATH = BASE_DIR / VECTOR_DB_PATH

# Fix for NEWS_ITEMS_DIR path resolution
NEWS_ITEMS_DIR = Path(NEWS_ITEMS_DIR)
if not NEWS_ITEMS_DIR.is_absolute():
    # Try to find the news-items directory in the parent directory
    parent_news_items = BASE_DIR.parent / "news-items"
    if parent_news_items.exists():
        NEWS_ITEMS_DIR = parent_news_items
    else:
        # Fallback to the original path
        NEWS_ITEMS_DIR = BASE_DIR.parent / NEWS_ITEMS_DIR

# Create directories if they don't exist
VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)

# Validate configuration
def validate_config():
    """Validate the configuration settings."""
    errors = []
    
    if DEFAULT_AI_PROVIDER not in ["ollama", "claude", "openai"]:
        errors.append(f"Invalid AI provider: {DEFAULT_AI_PROVIDER}")
    
    if DEFAULT_AI_PROVIDER == "openai" and not OPENAI_API_KEY:
        errors.append("OpenAI API key is required when using OpenAI provider")
    
    if DEFAULT_AI_PROVIDER == "claude" and not ANTHROPIC_API_KEY:
        errors.append("Anthropic API key is required when using Claude provider")
    
    if not NEWS_ITEMS_DIR.exists():
        errors.append(f"News items directory does not exist: {NEWS_ITEMS_DIR}")
    
    return errors 