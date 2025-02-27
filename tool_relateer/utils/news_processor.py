def fetch_article_from_url(url):
    """
    Fetch and parse a news article from a URL.
    
    Args:
        url (str): URL of the news article
        
    Returns:
        Article: Parsed article object or None if parsing fails
    """
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Fetching article from URL: {url}")
    
    try:
        # Send a GET request to the URL
        logger.info(f"Sending GET request to: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        # Check if the request was successful
        response.raise_for_status()
        logger.info(f"Request successful: {response.status_code}")
        
        # Parse the HTML content
        logger.info("Parsing HTML content")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the article title
        title = soup.find('title')
        title = title.text.strip() if title else "Unknown Title"
        logger.info(f"Extracted title: {title}")
        
        # Extract the article content
        # This is a simplified approach and may need to be adjusted for different news sites
        content_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        content = ' '.join([elem.text.strip() for elem in content_elements if elem.text.strip()])
        
        if not content:
            logger.warning("No content found using standard selectors, trying article tag")
            article_tag = soup.find('article')
            if article_tag:
                content = article_tag.text.strip()
        
        if not content:
            logger.warning("No content found using article tag, trying main tag")
            main_tag = soup.find('main')
            if main_tag:
                content = main_tag.text.strip()
        
        if not content:
            logger.error("Failed to extract content from the URL")
            return None
            
        logger.info(f"Extracted content length: {len(content)} characters")
        
        # Extract the publication date
        # This is a simplified approach and may need to be adjusted for different news sites
        date = None
        date_meta = soup.find('meta', property='article:published_time')
        if date_meta:
            date = date_meta.get('content')
            logger.info(f"Extracted date from meta tag: {date}")
        
        if not date:
            # Try to find a time element
            time_elem = soup.find('time')
            if time_elem and time_elem.get('datetime'):
                date = time_elem.get('datetime')
                logger.info(f"Extracted date from time element: {date}")
        
        # Extract the source
        source = urlparse(url).netloc
        logger.info(f"Extracted source: {source}")
        
        # Create and return the article object
        article = Article(
            id=None,  # Will be assigned later
            title=title,
            content=content,
            date=date,
            source=source,
            url=url
        )
        
        logger.info(f"Successfully created article object: {article.title}")
        return article
        
    except requests.exceptions.RequestException as e:
        logger.exception(f"Request error fetching URL {url}: {str(e)}")
        return None
    except Exception as e:
        logger.exception(f"Error fetching article from URL {url}: {str(e)}")
        return None 