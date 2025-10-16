#!/bin/bash

# Setup script for the Pharmacy API project

echo "Setting up the Pharmacy API development environment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Unix/Linux/Mac

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
fi

echo "Local setup complete. Pre-commit hooks are installed."
echo "To run the project, use the Docker scripts (e.g., scripts/run_docker.sh)."