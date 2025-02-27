#!/usr/bin/env python3
"""
Script to run the News Relations application.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Make sure we're in the correct directory
os.chdir(Path(__file__).resolve().parent)

# Import and run the Flask app
from app import app

if __name__ == "__main__":
    # Create required directories
    (Path(__file__).resolve().parent / "static").mkdir(exist_ok=True)
    
    # Get port from environment or use default
    # Using 5001 as default to avoid conflicts with AirPlay Receiver on macOS
    port = int(os.environ.get("PORT", 5001))
    
    # Start the app
    app.run(debug=True, host='0.0.0.0', port=port) 