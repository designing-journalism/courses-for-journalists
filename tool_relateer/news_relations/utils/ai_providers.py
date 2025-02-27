"""
Utilities for interacting with different AI providers.
"""

import json
import requests
from typing import Dict, Any, List, Optional, Union
import anthropic
import openai
from utils.config import (
    DEFAULT_AI_PROVIDER,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    ANTHROPIC_API_KEY,
    ANTHROPIC_MODEL
)

class AIProvider:
    """Base class for AI providers."""
    
    def __init__(self):
        self.provider_name = "base"
    
    def get_completion(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Get a completion from the AI provider.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            
        Returns:
            The AI response
        """
        raise NotImplementedError("Subclasses must implement get_completion")
    
    def generate_summary(self, article_content: str, max_length: int = 200) -> str:
        """
        Generate a concise summary of an article.
        
        Args:
            article_content: The content of the article to summarize
            max_length: Maximum length of the summary in characters
            
        Returns:
            A concise summary of the article
        """
        system_prompt = """
        You are an expert news summarizer. Your task is to create a concise, informative summary of a news article.
        The summary should capture the key points, main entities, and central narrative of the article.
        Keep the summary clear, objective, and focused on the most important information.
        """
        
        prompt = f"""
        Please summarize the following article in a concise paragraph:
        
        {article_content}
        
        Provide only the summary text without any additional commentary or formatting.
        """
        
        response = self.get_completion(prompt, system_prompt)
        
        # Clean up the response
        summary = response.strip()
        
        # Truncate if necessary
        if len(summary) > max_length:
            summary = summary[:max_length].rsplit(' ', 1)[0] + '...'
            
        return summary
    
    def analyze_relations(self, article_content: str, related_articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze the relationships between articles.
        
        Args:
            article_content: The content of the main article
            related_articles: List of related articles with metadata
            
        Returns:
            Analysis results
        """
        system_prompt = """
        You are an expert news analyst. Your task is to analyze the relationships between a main news article and a set of potentially related articles.
        Provide a detailed analysis of how these articles are related, including:
        1. Common themes, topics, or narratives
        2. Key entities (people, organizations, locations) that appear across multiple articles
        3. Temporal relationships (how events in different articles relate chronologically)
        4. Causal relationships (how events in one article might have influenced events in another)
        
        Format your response as JSON with the following structure:
        {
            "summary": "Brief summary of the relationships",
            "relationship_types": ["list", "of", "relationship", "types"],
            "key_entities": ["list", "of", "key", "entities"],
            "connections": [
                {
                    "article_id": "ID of related article",
                    "connection_type": "Type of connection",
                    "strength": "Strong/Medium/Weak",
                    "explanation": "Brief explanation of the connection"
                }
            ]
        }
        """
        
        # Format the related articles for the prompt
        related_articles_text = "\n\n".join([
            f"RELATED ARTICLE {i+1} (ID: {article['id']}):\nTitle: {article.get('title', 'Unknown')}\nDate: {article.get('date', 'Unknown')}\nContent: {article.get('content', 'No content')}"
            for i, article in enumerate(related_articles)
        ])
        
        prompt = f"""
        MAIN ARTICLE:
        {article_content}
        
        RELATED ARTICLES:
        {related_articles_text}
        
        Analyze the relationships between the main article and the related articles. 
        Provide your analysis in the JSON format specified in the instructions.
        """
        
        response = self.get_completion(prompt, system_prompt)
        
        # Extract JSON from response
        try:
            # Find JSON in the response (it might be wrapped in markdown code blocks)
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                return {"error": "No valid JSON found in response", "raw_response": response}
        except Exception as e:
            return {"error": str(e), "raw_response": response}


class OllamaProvider(AIProvider):
    """Provider for Ollama API."""
    
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL):
        super().__init__()
        self.provider_name = "ollama"
        self.base_url = base_url
        self.model = model
    
    def get_completion(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Get a completion from Ollama."""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            return f"Error: {str(e)}"


class ClaudeProvider(AIProvider):
    """Provider for Anthropic Claude API."""
    
    def __init__(self, api_key: str = ANTHROPIC_API_KEY, model: str = ANTHROPIC_MODEL):
        super().__init__()
        self.provider_name = "claude"
        self.api_key = api_key
        self.model = model
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def get_completion(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Get a completion from Claude."""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                system=system_prompt if system_prompt else "",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error: {str(e)}"


class OpenAIProvider(AIProvider):
    """Provider for OpenAI API."""
    
    def __init__(self, api_key: str = OPENAI_API_KEY, model: str = OPENAI_MODEL):
        super().__init__()
        self.provider_name = "openai"
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(api_key=api_key)
    
    def get_completion(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Get a completion from OpenAI."""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"


def get_ai_provider(provider_name: Optional[str] = None) -> AIProvider:
    """
    Get an AI provider instance.
    
    Args:
        provider_name: Name of the provider (ollama, claude, openai)
        
    Returns:
        An AIProvider instance
    """
    provider_name = provider_name or DEFAULT_AI_PROVIDER
    
    if provider_name == "ollama":
        return OllamaProvider()
    elif provider_name == "claude":
        return ClaudeProvider()
    elif provider_name == "openai":
        return OpenAIProvider()
    else:
        raise ValueError(f"Unknown AI provider: {provider_name}") 