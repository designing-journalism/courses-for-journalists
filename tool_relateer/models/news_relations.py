def process_url(self, url):
    """
    Process a news article URL, find related articles, and analyze relationships.
    
    Args:
        url (str): URL of the news article to process
        
    Returns:
        dict: Dictionary containing the article, related articles, analysis, and visualizations
    """
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Processing URL: {url}")
    
    try:
        # Fetch the article from the URL
        logger.info(f"Fetching article from URL: {url}")
        article = fetch_article_from_url(url)
        
        if not article:
            logger.error(f"Failed to fetch article from URL: {url}")
            return None
            
        logger.info(f"Successfully fetched article: {article.title}")
        
        # Ensure the article has a unique ID
        if not article.id:
            article.id = str(uuid.uuid4())
            logger.info(f"Generated new ID for article: {article.id}")
        
        # Temporarily add the article to the vector store for comparison
        logger.info("Checking if article already exists in vector store")
        similar_docs = self.embedding_manager.search(article.content, top_k=1)
        
        # Check if this is an exact match (same article)
        is_new_article = True
        if similar_docs and similar_docs[0][1] > 0.98:  # Similarity threshold
            logger.info(f"Article already exists in vector store with similarity {similar_docs[0][1]}")
            is_new_article = False
        else:
            logger.info("Article is new, adding temporarily to vector store")
            # Add the article to the vector store temporarily
            article.metadata = article.metadata or {}
            article.metadata['temporary'] = True
            article.is_new = True
            self.embedding_manager.add_document(article)
        
        # Find related articles
        logger.info("Finding related articles")
        related_articles = self.find_related_articles(article)
        logger.info(f"Found {len(related_articles)} related articles")
        
        # Analyze relationships
        logger.info("Analyzing relationships between articles")
        analysis = self.analyze_article_relations(article, related_articles)
        logger.info("Relationship analysis complete")
        
        # Create visualizations
        logger.info("Creating visualizations")
        visualizations = self.visualizer.create_visualizations(article, related_articles, analysis)
        logger.info("Visualizations created")
        
        return {
            'article': article,
            'related_articles': related_articles,
            'analysis': analysis,
            'visualizations': visualizations
        }
    except Exception as e:
        logger.exception(f"Error processing URL {url}: {str(e)}")
        raise 