#!/usr/bin/env python3
"""
Script to create a .env file interactively.
"""

import os
import secrets
from pathlib import Path

def main():
    """Create a .env file interactively."""
    # Make sure we're in the correct directory
    os.chdir(Path(__file__).resolve().parent)
    
    # Check if .env file already exists
    env_path = Path(".env")
    if env_path.exists():
        overwrite = input(".env file already exists. Overwrite? (y/n): ")
        if overwrite.lower() != "y":
            print("Aborted.")
            return
    
    # Get user input
    print("\nCreating .env file...")
    print("Press Enter to use default values.\n")
    
    # Flask settings
    flask_app = input("Flask app name [app.py]: ") or "app.py"
    flask_env = input("Flask environment [development]: ") or "development"
    secret_key = input("Secret key [auto-generated]: ") or secrets.token_hex(16)
    
    # AI Provider settings
    default_ai_provider = input("Default AI provider (ollama, claude, openai) [ollama]: ") or "ollama"
    
    # Ollama settings
    ollama_base_url = input("Ollama base URL [http://localhost:11434]: ") or "http://localhost:11434"
    ollama_model = input("Ollama model [llama2]: ") or "llama2"
    
    # OpenAI settings
    openai_api_key = input("OpenAI API key []: ") or ""
    openai_model = input("OpenAI model [gpt-4o-mini]: ") or "gpt-4o-mini"
    
    # Anthropic settings
    anthropic_api_key = input("Anthropic API key []: ") or ""
    anthropic_model = input("Anthropic model [claude-3-sonnet-20240229]: ") or "claude-3-sonnet-20240229"
    
    # Vector database settings
    vector_db_path = input("Vector database path [./vector_db]: ") or "./vector_db"
    embedding_model = input("Embedding model [all-MiniLM-L6-v2]: ") or "all-MiniLM-L6-v2"
    
    # News data settings
    news_items_dir = input("News items directory [../news-items]: ") or "../news-items"
    
    # Create .env file
    with open(env_path, "w") as f:
        f.write(f"# Flask settings\n")
        f.write(f"FLASK_APP={flask_app}\n")
        f.write(f"FLASK_ENV={flask_env}\n")
        f.write(f"SECRET_KEY={secret_key}\n\n")
        
        f.write(f"# AI Provider settings\n")
        f.write(f"DEFAULT_AI_PROVIDER={default_ai_provider}\n\n")
        
        f.write(f"# Ollama settings\n")
        f.write(f"OLLAMA_BASE_URL={ollama_base_url}\n")
        f.write(f"OLLAMA_MODEL={ollama_model}\n\n")
        
        f.write(f"# OpenAI settings\n")
        f.write(f"OPENAI_API_KEY={openai_api_key}\n")
        f.write(f"OPENAI_MODEL={openai_model}\n\n")
        
        f.write(f"# Anthropic (Claude) settings\n")
        f.write(f"ANTHROPIC_API_KEY={anthropic_api_key}\n")
        f.write(f"ANTHROPIC_MODEL={anthropic_model}\n\n")
        
        f.write(f"# Vector database settings\n")
        f.write(f"VECTOR_DB_PATH={vector_db_path}\n")
        f.write(f"EMBEDDING_MODEL={embedding_model}\n\n")
        
        f.write(f"# News data settings\n")
        f.write(f"NEWS_ITEMS_DIR={news_items_dir}\n")
    
    print(f"\n.env file created at {env_path.absolute()}")
    print("You can now run the application with: python run.py")

if __name__ == "__main__":
    main() 