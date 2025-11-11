#!/bin/bash
# Quick setup script for GSC Sentiment Analysis

echo "================================================"
echo "GSC Sentiment Analysis - Quick Setup"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Download spaCy model
echo ""
echo "Downloading spaCy language model..."
python -m spacy download en_core_web_sm

# Download NLTK data
echo ""
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt'); nltk.download('brown'); nltk.download('punkt_tab')"

echo ""
echo "================================================"
echo "Setup complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Set up Google Search Console API credentials"
echo "2. Save credentials as 'credentials.json'"
echo "3. Run: python analyze.py --site https://yoursite.com"
echo ""
echo "See QUICKSTART.md for detailed instructions"
