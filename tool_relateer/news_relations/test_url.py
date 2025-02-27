#!/usr/bin/env python3
"""
Test script for URL processing.
"""

import sys
import logging
from models.news_relations import NewsRelationsManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_url(url):
    """Test processing a URL."""
    logger.info(f"Testing URL: {url}")
    
    try:
        # Initialize the manager
        manager = NewsRelationsManager()
        logger.info(f"Initialized NewsRelationsManager")
        
        # Process the URL
        logger.info(f"Processing URL...")
        result = manager.process_url(url)
        
        if "error" in result:
            logger.error(f"Error processing URL: {result['error']}")
            return
        
        # Log success
        logger.info(f"Successfully processed URL")
        logger.info(f"Article title: {result['article'].get('title', 'Unknown')}")
        logger.info(f"Found {len(result['related_articles'])} related articles")
        logger.info(f"Analysis summary: {result['analysis'].get('summary', 'No summary')}")
        
        # Check visualizations
        logger.info(f"Network path: {result['visualizations'].get('network_path', 'None')}")
        
        return result
    except Exception as e:
        logger.exception(f"Exception processing URL: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_url.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    test_url(url) 