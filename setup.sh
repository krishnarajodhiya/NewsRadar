#!/bin/bash
# NewsVerify AI - Setup and Run Script

echo "🚀 NewsVerify AI - Setup Script"
echo "================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python installation
echo "✓ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"
echo ""

# Create virtual environment
echo "✓ Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
fi
echo ""

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Install dependencies
echo "✓ Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi
echo ""

# Train model
echo "✓ Training ML model..."
cd backend
python3 train_model.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Model training completed${NC}"
    echo ""
else
    echo -e "${RED}✗ Model training failed${NC}"
    exit 1
fi
cd ..

echo ""
echo "================================"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "================================"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Start Flask Backend (in new terminal):"
echo -e "   ${YELLOW}cd backend && python3 app.py${NC}"
echo ""
echo "2. Open Frontend (in your browser):"
echo -e "   ${YELLOW}open frontend/index.html${NC}"
echo ""
echo "   Or serve with Python (in another new terminal):"
echo -e "   ${YELLOW}cd frontend && python3 -m http.server 8000${NC}"
echo -e "   Then visit ${YELLOW}http://localhost:8000${NC}"
echo ""
echo "3. Backend will be available at: ${YELLOW}http://localhost:5000${NC}"
echo ""
echo "Happy Fact-Checking! 🎉"
echo ""
