#!/usr/bin/env python3
"""
Script to test the AI providers.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Make sure we're in the correct directory
os.chdir(Path(__file__).resolve().parent)

# Import the AI providers
from utils.ai_providers import get_ai_provider, OllamaProvider, ClaudeProvider, OpenAIProvider
from utils.config import validate_config

def test_provider(provider_name):
    """Test an AI provider."""
    print(f"\nTesting {provider_name} provider...")
    
    try:
        # Get the provider
        provider = get_ai_provider(provider_name)
        
        # Test a simple completion
        prompt = "Summarize the following news article in one sentence: 'The government announced new climate policies today, including a carbon tax and incentives for renewable energy.'"
        system_prompt = "You are a helpful assistant that summarizes news articles concisely."
        
        print("Sending test prompt...")
        response = provider.get_completion(prompt, system_prompt)
        
        print("\nResponse:")
        print(f"{response}")
        
        print("\nTest completed successfully!")
        return True
    except Exception as e:
        print(f"\nError testing {provider_name} provider: {str(e)}")
        return False

def main():
    """Test the AI providers."""
    # Validate configuration
    config_errors = validate_config()
    if config_errors:
        print("Configuration errors:")
        for error in config_errors:
            print(f"  - {error}")
        print("\nPlease fix these errors and try again.")
        return
    
    # Get provider to test
    if len(sys.argv) > 1:
        provider_name = sys.argv[1].lower()
        if provider_name not in ["ollama", "claude", "openai", "all"]:
            print(f"Unknown provider: {provider_name}")
            print("Available providers: ollama, claude, openai, all")
            return
        
        if provider_name == "all":
            providers = ["ollama", "claude", "openai"]
        else:
            providers = [provider_name]
    else:
        providers = ["ollama"]  # Default to Ollama
    
    # Test each provider
    results = {}
    for provider in providers:
        results[provider] = test_provider(provider)
    
    # Print summary
    print("\n--- Test Results ---")
    for provider, success in results.items():
        status = "✅ Success" if success else "❌ Failed"
        print(f"{provider}: {status}")

if __name__ == "__main__":
    main() 