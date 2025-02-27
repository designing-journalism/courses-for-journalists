"""
Utilities for processing news articles from markdown files and web URLs.
"""

import os
import re
import csv
import json
import requests
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from utils.config import NEWS_ITEMS_DIR


def parse_markdown_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse a markdown file containing a news article.
    
    Args:
        file_path: Path to the markdown file
        
    Returns:
        Dictionary with article metadata and content
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Parse filename for date and title
        filename = file_path.name
        date_match = re.match(r'(\d{8})\.(.+)\.md', filename)
        
        if date_match:
            date_str = date_match.group(1)
            title_slug = date_match.group(2)
            
            # Format date
            date = datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")
            
            # Format title
            title = title_slug.replace('-', ' ')
        else:
            date = "Unknown"
            title = filename.replace('.md', '')
        
        # Parse CSV content
        parts = content.split(',', 4)
        if len(parts) >= 3:
            datetime_str = parts[0]
            csv_title = parts[1]
            article_content = parts[2]
            
            # Use CSV title if available
            if csv_title:
                title = csv_title
            
            # Extract category and URL if available
            category = parts[3] if len(parts) > 3 else "Unknown"
            url = parts[4] if len(parts) > 4 else ""
        else:
            datetime_str = date
            article_content = content
            category = "Unknown"
            url = ""
        
        return {
            "id": file_path.stem,
            "filename": file_path.name,
            "date": date,
            "datetime": datetime_str,
            "title": title,
            "content": article_content,
            "category": category,
            "url": url,
            "source": "markdown",
            "file_path": str(file_path)
        }
    except Exception as e:
        return {
            "id": file_path.stem,
            "filename": file_path.name,
            "error": str(e),
            "content": "",
            "source": "markdown",
            "file_path": str(file_path)
        }


def fetch_article_from_url(url: str) -> Dict[str, Any]:
    """
    Fetch and parse a news article from a URL.
    
    Args:
        url: URL of the news article
        
    Returns:
        Dictionary with article metadata and content
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Extract title
        title = soup.title.text.strip() if soup.title else "Unknown Title"
        
        # Extract date (this is a simple approach, might need customization for specific sites)
        date = "Unknown"
        date_meta = soup.find('meta', property='article:published_time')
        if date_meta:
            date_str = date_meta.get('content', '')
            if date_str:
                try:
                    date = datetime.fromisoformat(date_str.split('T')[0]).strftime("%Y-%m-%d")
                except:
                    pass
        
        # Extract content (this is a simple approach, might need customization for specific sites)
        content = ""
        article_tag = soup.find('article')
        if article_tag:
            paragraphs = article_tag.find_all('p')
            content = ' '.join([p.text.strip() for p in paragraphs])
        else:
            # Fallback to main content area
            main_content = soup.find('main') or soup.find(id='content') or soup.find(class_='content')
            if main_content:
                paragraphs = main_content.find_all('p')
                content = ' '.join([p.text.strip() for p in paragraphs])
        
        # If still no content, try a more general approach
        if not content:
            paragraphs = soup.find_all('p')
            content = ' '.join([p.text.strip() for p in paragraphs[:10]])  # Limit to first 10 paragraphs
        
        # Extract domain as category
        domain = urlparse(url).netloc
        
        return {
            "id": url,
            "date": date,
            "title": title,
            "content": content,
            "category": domain,
            "url": url,
            "source": "web"
        }
    except Exception as e:
        return {
            "id": url,
            "error": str(e),
            "content": "",
            "url": url,
            "source": "web"
        }


def save_article_to_collection(article: Dict[str, Any]) -> str:
    """
    Save an article to the collection as a markdown file.
    
    Args:
        article: Article dictionary with metadata and content
        
    Returns:
        Filename of the saved article
    """
    # Ensure the news items directory exists
    NEWS_ITEMS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Format the date for the filename
    date_str = article.get("date", datetime.now().strftime("%Y-%m-%d"))
    try:
        # Try to parse the date if it's in YYYY-MM-DD format
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        date_filename = date_obj.strftime("%Y%m%d")
    except ValueError:
        # If parsing fails, use current date
        date_filename = datetime.now().strftime("%Y%m%d")
    
    # Create a slug from the title
    title = article.get("title", "Untitled Article")
    title_slug = title.lower().replace(' ', '-')
    # Remove special characters
    title_slug = re.sub(r'[^a-z0-9-]', '', title_slug)
    
    # Create filename
    filename = f"{date_filename}.{title_slug}.md"
    file_path = NEWS_ITEMS_DIR / filename
    
    # Check if file already exists, if so, add a unique identifier
    if file_path.exists():
        filename = f"{date_filename}.{title_slug}-{article.get('id', '')[:8]}.md"
        file_path = NEWS_ITEMS_DIR / filename
    
    # Prepare content
    content = article.get("content", "")
    
    # Write to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename


def load_all_markdown_articles() -> List[Dict[str, Any]]:
    """
    Load all markdown articles from the news items directory.
    
    Returns:
        List of article dictionaries
    """
    articles = []
    
    if not NEWS_ITEMS_DIR.exists():
        return articles
    
    for file_path in NEWS_ITEMS_DIR.glob('*.md'):
        article = parse_markdown_file(file_path)
        articles.append(article)
    
    return articles


def get_article_by_filename(filename: str) -> Optional[Dict[str, Any]]:
    """
    Get an article by its filename.
    
    Args:
        filename: The filename of the article
        
    Returns:
        Article dictionary or None if not found
    """
    file_path = NEWS_ITEMS_DIR / filename
    if file_path.exists():
        return parse_markdown_file(file_path)
    return None 