"""
Flask application for news relations.
"""

import os
import json
from pathlib import Path
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, send_from_directory
from flask_cors import CORS

from models.news_relations import NewsRelationsManager
from utils.config import SECRET_KEY, validate_config
from utils.news_processor import load_all_markdown_articles
from utils.embeddings import EmbeddingManager

# Create Flask app
app = Flask(__name__)
app.secret_key = SECRET_KEY
CORS(app)

# Create static directory if it doesn't exist
static_dir = Path(__file__).resolve().parent / "static"
static_dir.mkdir(exist_ok=True)

# Create templates directory if it doesn't exist
templates_dir = Path(__file__).resolve().parent / "templates"
templates_dir.mkdir(exist_ok=True)

# Initialize news relations manager
news_manager = NewsRelationsManager()
# Initialize embedding manager for direct access to document count
embedding_manager = EmbeddingManager()

@app.route('/')
def index():
    """Render the index page."""
    # Validate configuration
    config_errors = validate_config()
    if config_errors:
        return render_template('error.html', errors=config_errors)
    
    # Get list of articles
    articles = load_all_markdown_articles()
    
    # Sort by date (newest first)
    articles.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    # Get the count of documents in the vector store
    vector_store_count = embedding_manager.get_document_count()
    
    return render_template('index.html', articles=articles, vector_store_count=vector_store_count)

@app.route('/index_articles', methods=['POST'])
def index_articles():
    """Index all articles."""
    try:
        count = news_manager.index_all_articles()
        flash(f"Successfully indexed {count} articles", "success")
    except Exception as e:
        flash(f"Error indexing articles: {str(e)}", "error")
    
    return redirect(url_for('index'))

@app.route('/vector_store_info')
def vector_store_info():
    """Get information about the vector store."""
    try:
        count = embedding_manager.get_document_count()
        return render_template('vector_store_info.html', count=count)
    except Exception as e:
        flash(f"Error getting vector store information: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/article/<filename>')
def view_article(filename):
    """View an article and its related articles."""
    try:
        result = news_manager.process_file(filename)
        
        if "error" in result:
            flash(result["error"], "error")
            return redirect(url_for('index'))
        
        return render_template(
            'article.html',
            article=result["article"],
            summary=result.get("summary", ""),
            related_articles=result["related_articles"],
            analysis=result["analysis"],
            network_path=result["visualizations"]["network_path"]
        )
    except Exception as e:
        flash(f"Error processing article: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/url', methods=['GET', 'POST'])
def process_url():
    """Process a URL to find related articles."""
    if request.method == 'POST':
        url = request.form.get('url')
        app.logger.info(f"Processing URL: {url}")
        
        try:
            if not url:
                app.logger.error("No URL provided")
                flash('Please provide a URL', 'danger')
                return redirect(url_for('url'))
            
            # Process the URL
            app.logger.info(f"Initializing NewsRelationsManager")
            manager = NewsRelationsManager()
            
            app.logger.info(f"Calling manager.process_url with URL: {url}")
            result = manager.process_url(url)
            
            if not result:
                app.logger.error(f"Failed to process URL: {url} - No result returned")
                flash('Failed to process the URL. Please try again with a different URL.', 'danger')
                return redirect(url_for('url'))
            
            app.logger.info(f"URL processed successfully. Result keys: {result.keys()}")
            
            # Check if we have the expected data
            if 'article' not in result or not result['article']:
                app.logger.error(f"No article found in result: {result}")
                flash('Could not extract article from the URL. Please try a different news article.', 'danger')
                return redirect(url_for('url'))
                
            article = result['article']
            # Log article title, handling both dictionary and object cases
            if isinstance(article, dict):
                app.logger.info(f"Article found: {article.get('title', 'No title')}")
            else:
                try:
                    app.logger.info(f"Article found: {article.title}")
                except AttributeError:
                    app.logger.info(f"Article found but title not accessible")
            
            # Check if we have related articles
            if 'related_articles' not in result or not result['related_articles']:
                app.logger.warning(f"No related articles found for: {url}")
                # Continue processing even without related articles
            else:
                app.logger.info(f"Found {len(result['related_articles'])} related articles")
            
            # Show a success message based on whether the article was newly added
            if article.get('is_new', False):
                flash(f'Article "{article.get("title", "")}" has been added to your collection and related to existing articles.', 'success')
            else:
                flash(f'Article "{article.get("title", "")}" was already in your collection. Showing relations to existing articles.', 'info')
            
            # Render the result template with the processed data
            app.logger.info(f"Rendering url_result.html template")
            return render_template(
                'url_result.html',
                article=result['article'],
                summary=result.get('summary', ''),
                related_articles=result.get('related_articles', []),
                analysis=result.get('analysis', {}),
                visualizations=result.get('visualizations', {})
            )
        except Exception as e:
            app.logger.exception(f"Exception processing URL {url}: {str(e)}")
            flash(f'Error processing URL: {str(e)}', 'danger')
            return redirect(url_for('url'))
    
    return render_template('url_form.html')

@app.route('/api/article/<filename>')
def api_article(filename):
    """API endpoint for getting article data."""
    try:
        result = news_manager.process_file(filename)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/url', methods=['POST'])
def api_url():
    """API endpoint for processing a URL."""
    data = request.json
    url = data.get('url', '')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        result = news_manager.process_url(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/provider', methods=['POST'])
def api_set_provider():
    """API endpoint for setting the AI provider."""
    data = request.json
    provider = data.get('provider', '')
    
    if not provider:
        return jsonify({"error": "Provider is required"}), 400
    
    try:
        global news_manager
        news_manager = NewsRelationsManager(provider)
        return jsonify({"success": True, "provider": provider})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files."""
    return send_from_directory('static', path)

if __name__ == '__main__':
    # Create required directories
    (Path(__file__).resolve().parent / "static").mkdir(exist_ok=True)
    
    # Start the app
    app.run(debug=True, host='0.0.0.0', port=5000) 