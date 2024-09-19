#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Please install Python version 3.12 or higher."
    exit 1
fi

# Get the Python version
PY_VERSION=$(python3 --version | awk '{print $2}')
MAJOR=$(echo $PY_VERSION | cut -d. -f1)
MINOR=$(echo $PY_VERSION | cut -d. -f2)

# Check Python version (requires at least Python 3.12)
if [ "$MAJOR" -lt 3 ] || [ "$MAJOR" -eq 3 -a "$MINOR" -lt 12 ]; then
    echo "Python version must be at least 3.12. Please upgrade."
    exit 1
fi

echo "Python version is 3.12 or higher. Proceeding with setup..."

# Create a virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Ensure pip is installed and up-to-date
echo "Ensuring pip is up-to-date..."
pip install --upgrade pip

# Install pip-tools into the virtual environment
echo "Installing pip-tools..."
pip install pip-tools

# Compile dependencies from requirements.in
echo "Compiling requirements.txt from requirements.in..."
pip-compile requirements.in

# Install all dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Setup completed successfully."

# The environment is now activated; no need to run 'activate' again here
echo "The virtual environment is activated. You can now use it."