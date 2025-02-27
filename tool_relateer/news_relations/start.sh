#!/bin/bash
# Start script for the News Relations application

# Change to the script's directory
cd "$(dirname "$0")"

echo "========================================================"
echo "News Relations - Setup and Start Script"
echo "========================================================"
echo "This script will help you set up and start the News Relations application."
echo "========================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Please install pip3 and try again."
    exit 1
fi

# Check and install dependencies
echo "Checking required dependencies..."

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Found requirements.txt file."
    echo
    echo "Do you want to install/update dependencies from requirements.txt? (y/n)"
    read -r choice
    if [ "$choice" = "y" ]; then
        echo "Installing dependencies from requirements.txt..."
        pip3 install -r requirements.txt
        if [ $? -eq 0 ]; then
            echo "Dependencies installed successfully."
        else
            echo "Error installing dependencies. Please check your internet connection and try again."
            echo "You can continue, but the application may not work correctly."
            echo
            echo "Do you want to continue anyway? (y/n)"
            read -r choice
            if [ "$choice" != "y" ]; then
                echo "Setup aborted."
                exit 1
            fi
        fi
    else
        echo "Skipping dependency installation. The application may not work correctly."
    fi
else
    echo "requirements.txt not found. Cannot check dependencies."
    echo "The application may not work correctly without the required dependencies."
    echo
    echo "Do you want to continue anyway? (y/n)"
    read -r choice
    if [ "$choice" != "y" ]; then
        echo "Setup aborted."
        exit 1
    fi
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "No .env file found. Let's create one..."
    python3 create_env.py
else
    echo "Found .env file."
fi

# Check if vector_db directory exists
if [ ! -d "vector_db" ]; then
    echo "Vector database directory not found. Creating..."
    mkdir -p vector_db
    echo "Vector database directory created."
else
    echo "Found vector database directory."
fi

# Check if static directory exists
if [ ! -d "static" ]; then
    echo "Static directory not found. Creating..."
    mkdir -p static
    echo "Static directory created."
else
    echo "Found static directory."
fi

# Make scripts executable
echo "Making scripts executable..."
chmod +x app.py run.py init_db.py test_ai.py create_env.py make_executable.py start.py

# Initialize database
echo
echo "Do you want to initialize the vector database? (y/n)"
read -r choice
if [ "$choice" = "y" ]; then
    echo "Initializing vector database..."
    python3 init_db.py
fi

# Test AI providers
echo
echo "Do you want to test the AI providers? (y/n)"
read -r choice
if [ "$choice" = "y" ]; then
    echo "Which AI provider do you want to test? (ollama, claude, openai, all)"
    read -r provider
    if [[ "$provider" =~ ^(ollama|claude|openai|all)$ ]]; then
        echo "Testing $provider provider..."
        python3 test_ai.py "$provider"
    else
        echo "Invalid provider. Skipping test."
    fi
fi

# Run application
echo
echo "Do you want to start the application now? (y/n)"
read -r choice
if [ "$choice" = "y" ]; then
    echo "Starting the application..."
    python3 run.py
else
    echo
    echo "You can start the application later with:"
    echo "  python3 run.py"
    echo "  or"
    echo "  ./run.py"
fi

echo
echo "Setup complete!"
echo "========================================================" 