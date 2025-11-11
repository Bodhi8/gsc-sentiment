@echo off
REM Quick setup script for GSC Sentiment Analysis (Windows)

echo ================================================
echo GSC Sentiment Analysis - Quick Setup
echo ================================================
echo.

REM Check Python version
echo Checking Python version...
python --version

REM Install dependencies
echo.
echo Installing Python dependencies...
pip install -r requirements.txt

REM Download spaCy model
echo.
echo Downloading spaCy language model...
python -m spacy download en_core_web_sm

REM Download NLTK data
echo.
echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt'); nltk.download('brown'); nltk.download('punkt_tab')"

echo.
echo ================================================
echo Setup complete!
echo ================================================
echo.
echo Next steps:
echo 1. Set up Google Search Console API credentials
echo 2. Save credentials as 'credentials.json'
echo 3. Run: python analyze.py --site https://yoursite.com
echo.
echo See QUICKSTART.md for detailed instructions
pause
