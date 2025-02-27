#!/usr/bin/env python3
"""
Direct test script for URL processing.
"""

import sys
import logging
import traceback
from models.news_relations import NewsRelationsManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('direct_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def test_url(url):
    """Test processing a URL directly."""
    logger.info(f"Testing URL: {url}")
    
    try:
        # Initialize the manager
        logger.info("Initializing NewsRelationsManager")
        manager = NewsRelationsManager()
        
        # Process the URL
        logger.info(f"Processing URL: {url}")
        result = manager.process_url(url)
        
        if not result:
            logger.error("No result returned from process_url")
            return None
            
        # Log the result
        logger.info(f"Result keys: {result.keys()}")
        
        if 'article' in result and result['article']:
            article = result['article']
            if isinstance(article, dict):
                logger.info(f"Article title: {article.get('title', 'No title')}")
            else:
                # Try to access as an object attribute
                try:
                    logger.info(f"Article title: {article.title}")
                except AttributeError:
                    logger.info(f"Article: {article}")
        else:
            logger.error("No article in result")
            
        if 'related_articles' in result:
            logger.info(f"Found {len(result['related_articles'])} related articles")
        else:
            logger.warning("No related articles in result")
            
        if 'analysis' in result:
            logger.info(f"Analysis keys: {result['analysis'].keys() if result['analysis'] else 'None'}")
        else:
            logger.warning("No analysis in result")
            
        if 'visualizations' in result:
            logger.info(f"Visualizations keys: {result['visualizations'].keys() if result['visualizations'] else 'None'}")
        else:
            logger.warning("No visualizations in result")
            
        return result
    except Exception as e:
        logger.error(f"Exception processing URL: {str(e)}")
        logger.error(traceback.format_exc())
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python direct_test.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    result = test_url(url)
    
    if result:
        print("URL processed successfully")
    else:
        print("Failed to process URL")
        sys.exit(1) 