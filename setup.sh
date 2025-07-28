#!/bin/bash

echo "=== Phishing Email Detection Setup ==="
echo "Installing dependencies..."

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed. Please install Python 3 first."
    exit 1
fi

# Install requirements
if [ -f "requirements.txt" ]; then
    pip3 install --break-system-packages -r requirements.txt
elif [ -f "requirements/requirements.txt" ]; then
    pip3 install --break-system-packages -r requirements/requirements.txt
else
    echo "Error: requirements.txt not found"
    exit 1
fi

echo "Preprocessing data..."
python3 src/preprocess.py

echo "Training model..."
python3 src/train.py

echo "Testing prediction..."
python3 src/predict.py

echo ""
echo "=== Setup Complete! ==="
echo "You can now:"
echo "1. Run predictions: python3 src/predict.py"
echo "2. Start the web app: cd requirements && python3 app.py"
echo "3. Modify email text in src/predict.py to test different emails"