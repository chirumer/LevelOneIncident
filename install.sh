#!/bin/bash

# Installation script for Incident Response System

echo "=================================="
echo "Incident Response System Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✓ Python 3 found"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your Gemini API key!"
    echo "   Get your key from: https://makersuite.google.com/app/apikey"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

# Verify configuration
echo "Verifying configuration..."
python3 config.py

echo ""
echo "=================================="
echo "Installation Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your GEMINI_API_KEY"
echo "  2. Run: python3 test_incident.py (to test)"
echo "  3. Run: python3 web_server.py (to start server)"
echo ""
echo "For detailed setup instructions, see SETUP_GUIDE.md"
echo ""
