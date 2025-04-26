#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create static folder if it doesn't exist
if [ ! -d "app/static" ]; then
    echo "Creating static folder..."
    mkdir -p app/static
fi

# Move swagger.json to static folder
echo "Setting up Swagger UI..."
cp app/static/swagger.json app/static/swagger.json 2>/dev/null || :

# Create templates folder if it doesn't exist
if [ ! -d "app/templates" ]; then
    echo "Creating templates folder..."
    mkdir -p app/templates
fi

# Run the application
echo "Starting the application..."
export FLASK_APP=run.py
export FLASK_ENV=development
python run.py
