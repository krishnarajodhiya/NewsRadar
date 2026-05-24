#!/bin/bash
# NewsVerify AI - Quick Start Script

echo "🚀 Starting NewsVerify AI Application..."
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Running setup first..."
    bash setup.sh
    if [ $? -ne 0 ]; then
        echo "Setup failed. Please run setup.sh manually."
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

echo "✓ Virtual environment activated"
echo ""
echo "Starting Flask backend on http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

# Start backend
cd backend
python3 app.py
