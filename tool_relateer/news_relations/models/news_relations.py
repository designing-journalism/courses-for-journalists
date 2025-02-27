"""
Main model for managing news relations.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import uuid

from utils.embeddings import EmbeddingManager
from utils.ai_providers import get_ai_provider
from utils.news_processor import (
    parse_markdown_file,
    fetch_article_from_url,
    load_all_markdown_articles,
    get_article_by_filename,
    save_article_to_collection
)
from utils.visualizer import create_network_graph, create_plotly_graph
from utils.config import VECTOR_DB_PATH


class NewsRelationsManager:
    """
    Manager for finding and analyzing relationships between news articles.
    """
    
    def __init__(self, ai_provider_name: Optional[str] = None):
        """
        Initialize the news relations manager.
        
        Args:
            ai_provider_name: Name of the AI provider to use
        """
        self.embedding_manager = EmbeddingManager()
        self.ai_provider = get_ai_provider(ai_provider_name)
        self.relations_dir = VECTOR_DB_PATH / "relations"
        self.relations_dir.mkdir(parents=True, exist_ok=True)
    
    def index_all_articles(self) -> int:
        """
        Index all markdown articles.
        
        Returns:
            Number of articles indexed
        """
        articles = load_all_markdown_articles()
        
        # Extract text and metadata
        texts = []
        metadatas = []
        
        for article in articles:
            if "error" not in article:
                texts.append(article.get("content", ""))
                metadatas.append({
                    "id": article.get("id", ""),
                    "filename": article.get("filename", ""),
                    "date": article.get("date", ""),
                    "title": article.get("title", ""),
                    "category": article.get("category", ""),
                    "url": article.get("url", ""),
                    "source": article.get("source", "")
                })
        
        # Add to index
        if texts:
            self.embedding_manager.add_documents(texts, metadatas)
        
        return len(texts)
    
    def find_related_articles(
        self,
        article_content: str,
        article_metadata: Dict[str, Any],
        top_n: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find articles related to the given article.
        
        Args:
            article_content: Content of the article
            article_metadata: Metadata of the article
            top_n: Number of related articles to return
            
        Returns:
            List of related articles
        """
        # Search for related articles - get more than needed to allow for filtering
        results = self.embedding_manager.search(article_content, k=top_n * 2)
        
        # Filter out the article itself and near-duplicates
        article_id = article_metadata.get("id", "")
        results = [r for r in results if str(r.get("id", "")) != str(article_id) and r.get("similarity", 1.0) < 0.98]
        
        # Ensure diversity by limiting the number of articles from the same source/category
        source_count = {}
        category_count = {}
        diverse_results = []
        
        for result in results:
            source = result.get("source", "unknown")
            category = result.get("category", "unknown")
            
            # Limit to 2 articles per source and 3 per category
            if source_count.get(source, 0) < 2 and category_count.get(category, 0) < 3:
                diverse_results.append(result)
                source_count[source] = source_count.get(source, 0) + 1
                category_count[category] = category_count.get(category, 0) + 1
                
                # Break if we have enough diverse results
                if len(diverse_results) >= top_n:
                    break
        
        # If we don't have enough diverse results, add more from the filtered results
        if len(diverse_results) < top_n:
            remaining = [r for r in results if r not in diverse_results]
            diverse_results.extend(remaining[:top_n - len(diverse_results)])
        
        return diverse_results[:top_n]
    
    def analyze_article_relations(
        self,
        article_content: str,
        article_metadata: Dict[str, Any],
        related_articles: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze the relationships between the article and related articles.
        
        Args:
            article_content: Content of the article
            article_metadata: Metadata of the article
            related_articles: List of related articles
            
        Returns:
            Analysis results
        """
        # Use AI to analyze relationships
        analysis = self.ai_provider.analyze_relations(article_content, related_articles)
        
        # Save analysis
        self._save_analysis(article_metadata.get("id", ""), analysis, related_articles)
        
        return analysis
    
    def _save_analysis(
        self,
        article_id: str,
        analysis: Dict[str, Any],
        related_articles: List[Dict[str, Any]]
    ) -> None:
        """
        Save analysis results.
        
        Args:
            article_id: ID of the article
            analysis: Analysis results
            related_articles: List of related articles
        """
        # Create a record with analysis and related article IDs
        record = {
            "article_id": article_id,
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis,
            "related_article_ids": [str(a.get("id", "")) for a in related_articles]
        }
        
        # Ensure we're using a valid filename (article_id) and not a URL
        # Replace any invalid characters in the ID if necessary
        safe_id = str(article_id).replace(':', '_').replace('/', '_').replace('\\', '_')
        
        # Save to file
        file_path = self.relations_dir / f"{safe_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(record, f, indent=2)
    
    def get_saved_analysis(self, article_id: str) -> Optional[Dict[str, Any]]:
        """
        Get saved analysis for an article.
        
        Args:
            article_id: ID of the article
            
        Returns:
            Saved analysis or None if not found
        """
        file_path = self.relations_dir / f"{article_id}.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def process_url(self, url: str, top_n: int = 10) -> Dict[str, Any]:
        """
        Process a URL to find and analyze related articles.
        
        Args:
            url: URL of the article
            top_n: Number of related articles to return
            
        Returns:
            Dictionary with article, related articles, and analysis
        """
        # Fetch article from URL
        article = fetch_article_from_url(url)
        
        if "error" in article:
            return {"error": article["error"]}
        
        # Ensure the article has a unique ID if it doesn't already have one
        if not article.get("id"):
            article["id"] = str(uuid.uuid4())
        
        # Check if this article is already in the vector store
        is_new_article = True
        if self.embedding_manager.get_document_count() > 0:
            existing_docs = self.embedding_manager.search(article.get("content", ""), k=1)
            if existing_docs and existing_docs[0].get("similarity", 0) >= 0.98:  # Exact match found
                is_new_article = False
                # Use the existing article's metadata
                article["id"] = existing_docs[0].get("id", article["id"])
                article["filename"] = existing_docs[0].get("filename", "")
        
        # If it's a new article, save it to the collection and add to vector store
        if is_new_article:
            # Save article to collection
            filename = save_article_to_collection(article)
            article["filename"] = filename
            
            # Add to vector store permanently
            article_metadata = {
                "id": article.get("id", ""),
                "filename": filename,
                "title": article.get("title", ""),
                "date": article.get("date", ""),
                "category": article.get("category", ""),
                "url": article.get("url", ""),
                "source": article.get("source", "")
            }
            self.embedding_manager.add_document(article.get("content", ""), article_metadata)
        
        # Find related articles
        related_articles = self.find_related_articles(
            article.get("content", ""),
            article,
            top_n=top_n
        )
        
        # Analyze relationships
        analysis = self.analyze_article_relations(
            article.get("content", ""),
            article,
            related_articles
        )
        
        # Generate a summary of the article
        summary = self.ai_provider.generate_summary(article.get("content", ""))
        
        # Create visualizations
        network_path = create_network_graph(article, related_articles, analysis)
        plotly_graph = create_plotly_graph(article, related_articles, analysis)
        
        # Add a flag to indicate if this is a new article
        article["is_new"] = is_new_article
        
        return {
            "article": article,
            "summary": summary,
            "related_articles": related_articles,
            "analysis": analysis,
            "visualizations": {
                "network_path": network_path,
                "plotly_graph": plotly_graph
            }
        }
    
    def process_file(self, filename: str, top_n: int = 10) -> Dict[str, Any]:
        """
        Process a markdown file to find and analyze related articles.
        
        Args:
            filename: Filename of the article
            top_n: Number of related articles to return
            
        Returns:
            Dictionary with article, related articles, and analysis
        """
        # Get article from file
        article = get_article_by_filename(filename)
        
        if article is None or "error" in article:
            return {"error": "Article not found or error parsing file"}
        
        # Find related articles
        related_articles = self.find_related_articles(
            article.get("content", ""),
            article,
            top_n=top_n
        )
        
        # Analyze relationships
        analysis = self.analyze_article_relations(
            article.get("content", ""),
            article,
            related_articles
        )
        
        # Generate a summary of the article
        summary = self.ai_provider.generate_summary(article.get("content", ""))
        
        # Create visualizations
        network_path = create_network_graph(article, related_articles, analysis)
        plotly_graph = create_plotly_graph(article, related_articles, analysis)
        
        return {
            "article": article,
            "summary": summary,
            "related_articles": related_articles,
            "analysis": analysis,
            "visualizations": {
                "network_path": network_path,
                "plotly_graph": plotly_graph
            }
        } 