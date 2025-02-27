#!/usr/bin/env python3
"""
Script to initialize the vector database by indexing all articles.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Make sure we're in the correct directory
os.chdir(Path(__file__).resolve().parent)

# Import the news relations manager
from models.news_relations import NewsRelationsManager
from utils.config import validate_config

def main():
    """Initialize the vector database."""
    # Validate configuration
    config_errors = validate_config()
    if config_errors:
        print("Configuration errors:")
        for error in config_errors:
            print(f"  - {error}")
        print("\nPlease fix these errors and try again.")
        return
    
    # Create news relations manager
    print("Initializing news relations manager...")
    news_manager = NewsRelationsManager()
    
    # Index all articles
    print("Indexing articles...")
    count = news_manager.index_all_articles()
    
    print(f"\nSuccessfully indexed {count} articles.")
    print("The vector database is now ready to use.")

if __name__ == "__main__":
    main() 