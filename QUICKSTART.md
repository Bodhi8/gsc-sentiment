# GSC Sentiment Analysis - Quick Start Guide

## Prerequisites Checklist

Before running the analysis, ensure you have:

- [ ] Python 3.8+ installed
- [ ] pip package manager installed
- [ ] Git installed (for cloning the repository)
- [ ] Google account with Search Console access
- [ ] A verified website in Google Search Console

## Step-by-Step Setup

### 1. Install Python Dependencies

```bash
# Navigate to the project directory
cd gsc-sentiment

# Install required packages
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

### 2. Set Up Google Search Console API Access

#### A. Create a Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Click "Select a project" > "New Project"
3. Enter project name (e.g., "GSC Sentiment Analysis")
4. Click "Create"

#### B. Enable the Search Console API

1. In the Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google Search Console API"
3. Click on it and press "Enable"

#### C. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "+ CREATE CREDENTIALS" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: GSC Sentiment Tool
   - Support email: Your email
   - Scopes: Not required for this step
   - Test users: Add your email
4. For Application type, select "Desktop app"
5. Name: "GSC Sentiment Desktop Client"
6. Click "Create"

#### D. Download Credentials

1. Click the download icon next to your newly created OAuth client
2. Save the JSON file as `credentials.json` in the project root directory

### 3. First Run

```bash
# List available sites
python analyze.py

# You'll be prompted to authenticate in your browser
# Sign in with your Google account
# Grant the necessary permissions
```

This creates a `token.pickle` file for future runs (no need to re-authenticate).

### 4. Run Your First Analysis

```bash
# Replace with your actual site URL from the list
python analyze.py --site https://www.yoursite.com

# For more data (90 days instead of default 30)
python analyze.py --site https://www.yoursite.com --days 90

# Save to a custom output folder
python analyze.py --site https://www.yoursite.com --output reports/my-analysis
```

## Understanding Your First Results

After the analysis completes, check the `output` directory:

### Files Created:

1. **analysis_report.txt** - Start here! Human-readable summary
2. **detailed_analysis.csv** - Raw data for deeper analysis in Excel/Sheets
3. **analysis_summary.json** - Structured data for programmatic use
4. **Visualizations (PNG files)** - Charts and graphs

### Key Metrics to Look At:

1. **Sentiment Distribution**: Are most queries positive, negative, or neutral?
2. **Intent Distribution**: What are users trying to do?
3. **Strengths**: What's already working well
4. **Weaknesses**: What needs improvement
5. **Top Entities**: Which topics/entities drive traffic

## Common First-Time Issues

### "Credentials file not found"
- Make sure `credentials.json` is in the project root
- Check the filename (not `credentials (1).json` or similar)

### "Access denied" or "Permission denied"
- Ensure you're using the Google account that has access to Search Console
- Verify your site is verified in Search Console

### "No data found"
- Check the site URL format (include https://)
- Try a longer period: `--days 90`
- Verify your site has traffic in Search Console

### "Module not found" errors
- Run: `pip install -r requirements.txt`
- For spaCy model: `python -m spacy download en_core_web_sm`

## Next Steps

1. **Review the Report**: Read `analysis_report.txt` thoroughly
2. **Identify Quick Wins**: Look at the "Opportunities" section
3. **Prioritize**: Focus on high-impact items first
4. **Take Action**: Implement recommendations
5. **Re-run Analysis**: Check progress after changes (wait 2-4 weeks)

## Getting Help

If you encounter issues:

1. Check this guide again
2. Review the main README.md for detailed documentation
3. Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - Your Python version (`python --version`)

## Advanced Usage

### Analyze Multiple Sites

Create a bash script:

```bash
#!/bin/bash
for site in site1.com site2.com site3.com; do
  python analyze.py --site https://$site --output output/$site
done
```

### Automated Weekly Reports

Use cron (Linux/Mac) or Task Scheduler (Windows):

```bash
# Run every Monday at 9 AM
0 9 * * 1 cd /path/to/gsc-sentiment && python analyze.py --site https://yoursite.com
```

### Custom Analysis

Edit the Python modules directly for custom analysis:
- `sentiment_analyzer.py` - Add custom sentiment rules
- `entity_analyzer.py` - Customize entity extraction
- `insights_generator.py` - Add custom insights

Happy analyzing!
