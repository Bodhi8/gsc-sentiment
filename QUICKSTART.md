# Quick Start Guide

Get up and running with GSC Sentiment Analyzer in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Google Cloud account (free tier works)
- Google Search Console property with data

## Step 1: Clone and Install (2 minutes)

```bash
# Clone the repository
git clone https://github.com/Bodhi8/gsc-sentiment.git
cd gsc-sentiment

# Run setup script (installs dependencies)
python setup.py
```

## Step 2: Google Cloud Setup (2 minutes)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable the **Google Search Console API**
4. Create a Service Account:
   - Navigate to: IAM & Admin → Service Accounts
   - Click "Create Service Account"
   - Name it (e.g., "gsc-sentiment-analyzer")
   - Skip role assignment (click Continue twice)
   - Click "Create Key" → JSON
   - Download the JSON file

5. Add Service Account to Search Console:
   - Copy the service account email (looks like: `name@project.iam.gserviceaccount.com`)
   - Go to [Search Console](https://search.google.com/search-console)
   - Select your property
   - Settings → Users and permissions
   - Add User → paste the email → Full permissions

## Step 3: Configure (1 minute)

Edit the `.env` file:

```bash
# Update these values
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/downloaded-credentials.json
SITE_URL=https://yourdomain.com
START_DATE=2024-01-01
END_DATE=2024-12-31
```

**Note**: Use the exact URL shown in Search Console (with or without www, http/https).

## Step 4: Run Analysis (30 seconds)

```bash
# Run the analyzer
python gsc_sentiment_analyzer.py
```

That's it! Results will be saved to the `outputs/` directory.

## What You Get

After running, check the `outputs/` folder for:

1. **insights_report_[timestamp].txt** - Human-readable analysis
2. **full_analysis_[timestamp].csv** - All data with sentiment scores
3. **strengths_[timestamp].csv** - Your top-performing content
4. **weaknesses_[timestamp].csv** - Areas needing improvement
5. **Visualizations** - Charts showing sentiment distribution and trends
6. **interactive_dashboard_[timestamp].html** - Interactive charts (open in browser)

## Quick Tips

### View the Interactive Dashboard

```bash
# Open in your default browser (macOS)
open outputs/interactive_dashboard_*.html

# Linux
xdg-open outputs/interactive_dashboard_*.html

# Windows
start outputs/interactive_dashboard_*.html
```

### Run Examples

```bash
python examples.py
# Then choose from 5 different example analyses
```

### Common Issues

**"No data available"**
- Check date range in .env
- Verify site URL matches Search Console exactly
- Ensure property has data for the date range

**"Authentication error"**
- Verify credentials file path in .env
- Ensure service account is added to Search Console
- Check API is enabled in Google Cloud

**"spaCy model not found"** (warning only)
- Entity extraction will be limited
- Install with: `python -m spacy download en_core_web_sm`
- Not critical - sentiment analysis still works

## Next Steps

1. **Read the insights report** - Start with `insights_report_*.txt`
2. **Explore the dashboard** - Open the HTML file in a browser
3. **Review strengths** - What's working well?
4. **Address weaknesses** - What needs improvement?
5. **Check entities** - What topics are you known for?

## Learning More

- **Full documentation**: See [README.md](README.md)
- **API reference**: See [API_REFERENCE.md](API_REFERENCE.md)
- **In-depth guide**: See [GUIDE.md](GUIDE.md)
- **Examples**: Run `python examples.py` for various use cases

## Sample Output

Here's what a typical insights report looks like:

```
================================================================================
GOOGLE SEARCH CONSOLE SENTIMENT ANALYSIS REPORT
================================================================================

OVERALL STATISTICS
--------------------------------------------------------------------------------
Total queries analyzed: 1,234
Total clicks: 45,678
Average sentiment score: 0.125

SENTIMENT DISTRIBUTION
--------------------------------------------------------------------------------
Positive: 456 (37.0%)
Neutral: 678 (54.9%)
Negative: 100 (8.1%)

TOP STRENGTHS
--------------------------------------------------------------------------------
Query: best practices for python testing
  - Sentiment: 0.765 (positive)
  - Performance Score: 87.3/100
  ...
```

## Support

Having issues? Check:
1. This Quick Start Guide
2. [README.md](README.md) - Detailed setup instructions
3. [GitHub Issues](https://github.com/Bodhi8/gsc-sentiment/issues) - Report bugs

## Advanced Usage

Once comfortable with the basics, try:

- **Comparative analysis**: Compare different time periods
- **Country analysis**: Analyze by geographic region
- **Custom filters**: Filter by specific metrics
- **API integration**: Use as a Python module in your own scripts

See [examples.py](examples.py) for code samples!
