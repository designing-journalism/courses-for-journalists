#!/usr/bin/env python3
"""
Start script for the News Relations application.
This script helps users get started with the application by setting up the environment and running the application.
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed and install them if needed."""
    print("Checking required dependencies...")
    
    # List of required packages
    required_packages = [
        "flask", "flask-cors", "python-dotenv", "requests", "numpy", 
        "scikit-learn", "sentence-transformers", "faiss-cpu", "langchain",
        "langchain-community", "anthropic", "openai", "beautifulsoup4", 
        "lxml", "plotly", "networkx", "pyvis"
    ]
    
    # Check if requirements.txt exists
    req_path = Path("requirements.txt")
    if req_path.exists():
        print("Found requirements.txt file.")
        
        # Ask user if they want to install dependencies
        print("\nDo you want to install/update dependencies from requirements.txt? (y/n)")
        choice = input("> ").lower()
        if choice == "y":
            print("Installing dependencies from requirements.txt...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("Dependencies installed successfully.")
            return True
    
    # If requirements.txt doesn't exist or user chose not to use it,
    # check individual packages
    missing_packages = []
    for package in required_packages:
        # Convert package name to import name (e.g., flask-cors -> flask_cors)
        import_name = package.replace("-", "_")
        
        # Check if package is installed
        if importlib.util.find_spec(import_name) is None:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing dependencies: {', '.join(missing_packages)}")
        print("Do you want to install these dependencies? (y/n)")
        choice = input("> ").lower()
        if choice == "y":
            for package in missing_packages:
                print(f"Installing {package}...")
                subprocess.run([sys.executable, "-m", "pip", "install", package])
            print("Dependencies installed successfully.")
            return True
        else:
            print("Warning: The application may not work without these dependencies.")
            return False
    else:
        print("All required dependencies are installed.")
        return True

def check_environment():
    """Check if the environment is properly set up."""
    # Check if .env file exists
    env_path = Path(".env")
    if not env_path.exists():
        print("No .env file found. Let's create one...")
        subprocess.run([sys.executable, "create_env.py"])
    else:
        print("Found .env file.")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("Warning: python-dotenv is not installed. Environment variables may not be loaded correctly.")
    
    # Check if vector_db directory exists
    vector_db_path = Path("vector_db")
    if not vector_db_path.exists():
        print("Vector database directory not found. Creating...")
        vector_db_path.mkdir(parents=True, exist_ok=True)
        print("Vector database directory created.")
    else:
        print("Found vector database directory.")
    
    # Check if static directory exists
    static_path = Path("static")
    if not static_path.exists():
        print("Static directory not found. Creating...")
        static_path.mkdir(parents=True, exist_ok=True)
        print("Static directory created.")
    else:
        print("Found static directory.")

def make_scripts_executable():
    """Make the Python scripts executable."""
    print("Making scripts executable...")
    subprocess.run([sys.executable, "make_executable.py"])

def initialize_database():
    """Initialize the vector database."""
    print("\nDo you want to initialize the vector database? (y/n)")
    choice = input("> ").lower()
    if choice == "y":
        print("Initializing vector database...")
        subprocess.run([sys.executable, "init_db.py"])

def test_ai_providers():
    """Test the AI providers."""
    print("\nDo you want to test the AI providers? (y/n)")
    choice = input("> ").lower()
    if choice == "y":
        print("Which AI provider do you want to test? (ollama, claude, openai, all)")
        provider = input("> ").lower()
        if provider in ["ollama", "claude", "openai", "all"]:
            print(f"Testing {provider} provider...")
            subprocess.run([sys.executable, "test_ai.py", provider])
        else:
            print("Invalid provider. Skipping test.")

def run_application():
    """Run the application."""
    print("\nDo you want to start the application now? (y/n)")
    choice = input("> ").lower()
    if choice == "y":
        print("Starting the application...")
        subprocess.run([sys.executable, "run.py"])
    else:
        print("\nYou can start the application later with:")
        print("  python run.py")
        print("  or")
        print("  ./run.py (if you made the scripts executable)")

def main():
    """Main function."""
    # Make sure we're in the correct directory
    os.chdir(Path(__file__).resolve().parent)
    
    print("=" * 60)
    print("News Relations - Setup and Start Script")
    print("=" * 60)
    print("This script will help you set up and start the News Relations application.")
    print("=" * 60)
    
    # Check dependencies
    dependencies_ok = check_dependencies()
    if not dependencies_ok:
        print("\nWarning: Some dependencies are missing. The application may not work correctly.")
        print("Please install the required dependencies and try again.")
        print("You can install them with: pip install -r requirements.txt")
        
        # Ask if user wants to continue anyway
        print("\nDo you want to continue anyway? (y/n)")
        choice = input("> ").lower()
        if choice != "y":
            print("Setup aborted.")
            return
    
    # Check environment
    check_environment()
    
    # Make scripts executable
    make_scripts_executable()
    
    # Initialize database
    initialize_database()
    
    # Test AI providers
    test_ai_providers()
    
    # Run application
    run_application()
    
    print("\nSetup complete!")
    print("=" * 60)

if __name__ == "__main__":
    main() 