# News Relations

A Flask-based application for finding and visualizing relationships between news articles using AI and vector embeddings.

## Features

- Find semantically similar news articles using vector embeddings
- Analyze relationships between articles using AI (Ollama, Claude, or OpenAI)
- Visualize relationships with interactive network graphs
- Process both existing markdown files and new URLs
- Web interface for browsing and analyzing articles
- API endpoints for integration with other systems

## How Articles Are Related

The application uses a two-step process to determine article relationships:

1. **Vector Embeddings for Semantic Similarity**: Articles are converted into high-dimensional vectors using a pre-trained Sentence Transformer model. The system calculates cosine similarity scores to find semantically similar articles efficiently, even with large datasets. We use FAISS for fast similarity search.

2. **AI Analysis for Relationship Types**: After identifying similar articles, the AI analyzes them to identify common themes, key entities, temporal and causal relationships. It categorizes each relationship type and strength, providing detailed explanations.

This two-step approach combines the efficiency of vector embeddings with the nuanced understanding of AI, allowing the system to identify both obvious and subtle connections between news articles.

For more detailed information about how article relationships are determined, see the [detailed documentation](docs/article_relations.md).

## Requirements

- Python 3.8+
- Flask
- Sentence Transformers
- FAISS
- LangChain
- Ollama (optional, for local AI)
- OpenAI API key (optional)
- Anthropic API key (optional)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd news-relations
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```

4. Edit the `.env` file to configure your settings:
   - Set your preferred AI provider (ollama, claude, or openai)
   - Add API keys if using Claude or OpenAI
   - Configure paths and other settings

## Quick Start

The easiest way to get started is to use one of the provided start scripts:

### Using Python

```
python start.py
```

This interactive script will:
1. Check and install required dependencies
2. Check if your environment is properly set up
3. Create a `.env` file if needed
4. Make all scripts executable
5. Initialize the vector database (optional)
6. Test the AI providers (optional)
7. Start the application (optional)

### Using Shell Script (Unix/Mac)

```
./start.sh
```

This shell script provides the same functionality as the Python script but in a shell environment.

## Troubleshooting

If you encounter errors when running the application, it's likely due to missing dependencies. The start scripts will help you install the required dependencies, but you can also install them manually:

```
pip install -r requirements.txt
```

Common issues:
- `ModuleNotFoundError: No module named 'faiss'` - Install with `pip install faiss-cpu`
- `ModuleNotFoundError: No module named 'anthropic'` - Install with `pip install anthropic`
- `ModuleNotFoundError: No module named 'flask_cors'` - Install with `pip install flask-cors`
- **Port 5000 in use on macOS** - The application now uses port 5001 by default to avoid conflicts with AirPlay Receiver on macOS. If you still encounter port conflicts, you can set a different port in the `.env` file or by setting the `PORT` environment variable.

## Manual Usage

If you prefer to set up and run the application manually:

1. Create a `.env` file:
   ```
   python create_env.py
   ```

2. Make scripts executable:
   ```
   python make_executable.py
   ```

3. Initialize the vector database:
   ```
   python init_db.py
   ```

4. Test the AI providers:
   ```
   python test_ai.py [provider]
   ```
   Where `[provider]` is one of: ollama, claude, openai, all

5. Start the Flask application:
   ```
   python run.py
   ```

6. Open your browser and navigate to:
   ```
   http://localhost:5001
   ```
   Note: The application now uses port 5001 by default instead of 5000 to avoid conflicts with AirPlay Receiver on macOS.

## Directory Structure

- `app.py`: Main Flask application
- `models/`: Contains the main business logic
- `utils/`: Utility functions and helpers
- `templates/`: HTML templates for the web interface
- `static/`: Static files and generated visualizations
- `vector_db/`: Directory for storing vector embeddings and analysis results

## AI Providers

The application supports three AI providers:

1. **Ollama (Local)**
   - Runs locally on your machine
   - Requires Ollama to be installed and running
   - No API key required
   - Good for privacy and offline use

2. **Claude (Anthropic)**
   - Cloud-based AI service
   - Requires an Anthropic API key
   - Excellent analysis quality

3. **OpenAI**
   - Cloud-based AI service
   - Requires an OpenAI API key
   - Excellent analysis quality

## API Endpoints

- `GET /api/article/<filename>`: Get analysis for a specific article
- `POST /api/url`: Analyze a URL and find related articles
- `POST /api/provider`: Change the AI provider

## License

MIT

## Credits

- [Flask](https://flask.palletsprojects.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [LangChain](https://langchain.com/)
- [Pyvis](https://pyvis.readthedocs.io/)
- [Plotly](https://plotly.com/) 