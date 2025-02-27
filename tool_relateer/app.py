import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from models.news_relations import NewsRelationsManager
from utils.embedding_manager import EmbeddingManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('flask_app.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_for_flash_messages')
app.logger.setLevel(logging.INFO)
app.logger.info("Flask application starting")

@app.route('/process_url', methods=['POST'])
def process_url():
    url = request.form.get('url')
    app.logger.info(f"Processing URL: {url}")
    
    try:
        if not url:
            app.logger.error("No URL provided")
            flash('Please provide a URL', 'danger')
            return redirect(url_for('url_form'))
        
        # Process the URL
        app.logger.info(f"Initializing NewsRelationsManager")
        manager = NewsRelationsManager()
        
        app.logger.info(f"Calling manager.process_url with URL: {url}")
        result = manager.process_url(url)
        
        if not result:
            app.logger.error(f"Failed to process URL: {url} - No result returned")
            flash('Failed to process the URL. Please try again with a different URL.', 'danger')
            return redirect(url_for('url_form'))
        
        app.logger.info(f"URL processed successfully. Result keys: {result.keys()}")
        
        # Check if we have the expected data
        if 'article' not in result or not result['article']:
            app.logger.error(f"No article found in result: {result}")
            flash('Could not extract article from the URL. Please try a different news article.', 'danger')
            return redirect(url_for('url_form'))
            
        app.logger.info(f"Article found: {result['article'].title}")
        
        # Check if we have related articles
        if 'related_articles' not in result or not result['related_articles']:
            app.logger.warning(f"No related articles found for: {url}")
            # Continue processing even without related articles
        else:
            app.logger.info(f"Found {len(result['related_articles'])} related articles")
        
        # Render the result template with the processed data
        app.logger.info(f"Rendering url_result.html template")
        return render_template(
            'url_result.html',
            article=result['article'],
            related_articles=result.get('related_articles', []),
            analysis=result.get('analysis', {}),
            visualizations=result.get('visualizations', {})
        )
    except Exception as e:
        app.logger.exception(f"Exception processing URL {url}: {str(e)}")
        flash(f'Error processing URL: {str(e)}', 'danger')
        return redirect(url_for('url_form')) 