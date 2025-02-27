# How Articles Are Related in News Relations

This document provides a detailed explanation of how the News Relations application determines relationships between articles.

## Overview

The News Relations application uses a sophisticated two-step process to identify and analyze relationships between news articles:

1. **Vector Embeddings** for finding semantically similar articles
2. **AI Analysis** for determining the specific types and strengths of relationships

This approach combines the efficiency of vector-based similarity search with the nuanced understanding of AI to provide comprehensive insights into article relationships.

## Vector Embeddings for Semantic Similarity

### What are Vector Embeddings?

Vector embeddings are numerical representations of text in a high-dimensional space. Each article is converted into a vector (essentially a list of numbers) that captures the semantic meaning of the content. Similar articles will have vectors that are close to each other in this high-dimensional space.

### How We Generate Embeddings

The News Relations application uses the Sentence Transformers library with a pre-trained model to generate embeddings:

1. The article text is processed and tokenized
2. The pre-trained model converts the text into a dense vector (typically 384 or 768 dimensions)
3. These vectors are stored in a FAISS index for efficient similarity search

### Finding Similar Articles

When you submit a new article (either by URL or from a file), the system:

1. Generates a vector embedding for the new article
2. Compares this vector to all existing article vectors in the collection
3. Calculates a similarity score (cosine similarity) between the new article and each existing article
4. Ranks the articles by similarity score
5. Returns the top N most similar articles (default is 10)

The similarity score ranges from 0 to 1, where:
- 1.0 = identical content
- 0.8-0.99 = very similar content
- 0.6-0.79 = moderately similar content
- 0.4-0.59 = somewhat similar content
- Below 0.4 = minimally related content

This vector-based approach is extremely efficient and can search through thousands of articles in milliseconds.

## AI Analysis for Relationship Types

After finding semantically similar articles, the system uses AI to perform a deeper analysis of the relationships.

### The AI Analysis Process

1. The system sends the main article and the most similar articles to the AI provider (Ollama, Claude, or OpenAI)
2. The AI is given a specific prompt that asks it to analyze the relationships between the articles
3. The AI performs a comprehensive analysis to identify various types of relationships

### What the AI Analyzes

The AI looks for several types of relationships:

1. **Thematic Relationships**:
   - Common topics or themes
   - Shared narratives or storylines
   - Similar subject matter

2. **Entity Relationships**:
   - Same people mentioned across articles
   - Same organizations or institutions
   - Same locations or geographical areas

3. **Temporal Relationships**:
   - Chronological connections (before/after)
   - Articles covering different stages of the same event
   - Follow-up stories or developments

4. **Causal Relationships**:
   - How events in one article might have influenced events in another
   - Cause-and-effect connections between stories

5. **Perspective Relationships**:
   - Different viewpoints on the same issue
   - Complementary or contradictory perspectives
   - Bias or stance differences

### AI Output Format

The AI returns a structured analysis that includes:

- A summary of the overall relationships
- A list of relationship types identified
- Key entities that appear across multiple articles
- Specific connections between the main article and each related article, including:
  - The type of connection
  - The strength of the connection (Strong, Medium, or Weak)
  - A detailed explanation of the connection

## Visualization of Relationships

The system visualizes these relationships in two ways:

1. **Network Graph**: An interactive visualization showing the main article and its connections to related articles, with edges colored according to relationship strength.

2. **Relationship Cards**: Each related article is displayed with its connection type, strength, and explanation.

## Technical Implementation

The relationship analysis process is implemented in the following components:

- `EmbeddingManager` class in `utils/embeddings.py`: Handles vector embeddings and similarity search
- `NewsRelationsManager.find_related_articles()` in `models/news_relations.py`: Finds similar articles using vector embeddings
- `AIProvider.analyze_relations()` in `utils/ai_providers.py`: Performs AI analysis of relationships
- `NewsRelationsManager.analyze_article_relations()` in `models/news_relations.py`: Coordinates the AI analysis process

## Conclusion

The combination of vector embeddings and AI analysis provides a powerful system for identifying and understanding relationships between news articles. This approach balances computational efficiency with deep semantic understanding, allowing users to discover connections that might not be immediately obvious.

By using this two-step process, the News Relations application can handle large collections of articles while still providing nuanced insights into how different stories relate to each other. 