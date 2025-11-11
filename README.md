# GSC Sentiment Analysis Tool

A comprehensive sentiment analysis tool for Google Search Console data that helps identify site strengths, weaknesses, and AI citation opportunities.

## Overview

This tool analyzes your Google Search Console data to provide insights about:
- **Sentiment Analysis**: Understand the emotional context of search queries driving traffic
- **Search Intent Classification**: Identify informational, commercial, navigational, and problem-solving queries
- **Entity Extraction**: Discover key entities that drive traffic and could improve AI citations
- **Performance Insights**: Identify strengths, weaknesses, and optimization opportunities
- **AI Citation Strategy**: Get recommendations for improving your site's potential for AI-powered search citations

## Features

### 1. Sentiment Analysis
- Analyzes sentiment (positive, negative, neutral) of search queries
- Measures polarity and subjectivity of queries
- Correlates sentiment with performance metrics (clicks, CTR, position)

### 2. Search Intent Classification
- Categorizes queries into:
  - **Informational**: How-to and knowledge-seeking queries
  - **Commercial**: Buying-intent and comparison queries
  - **Problem-Solving**: Troubleshooting and fix-related queries
  - **Navigational**: Brand and direct navigation queries

### 3. Entity Extraction & AI Citations
- Extracts named entities (people, organizations, products, locations)
- Identifies entities that drive the most traffic
- Provides recommendations for improving AI citation potential
- Suggests structured data implementations

### 4. Insights Generation
- **Strengths**: What your site does well
- **Weaknesses**: Areas needing improvement
- **Opportunities**: Untapped traffic potential
- **AI Strategy**: How to optimize for AI-powered search

### 5. Visualizations
- Sentiment distribution charts
- Intent analysis graphs
- Performance comparisons
- Entity traffic analysis
- CTR vs Position scatter plots

## Installation

### Prerequisites
- Python 3.8 or higher
- Google Search Console account with verified site
- Google Cloud Project with Search Console API enabled

### Step 1: Clone the Repository
```bash
git clone https://github.com/Bodhi8/gsc-sentiment.git
cd gsc-sentiment
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Download spaCy Model
```bash
python -m spacy download en_core_web_sm
```

### Step 4: Set Up Google Search Console API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Search Console API**
4. Create **OAuth 2.0 credentials**:
   - Go to APIs & Services > Credentials
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as application type
   - Download the credentials JSON file
5. Save the credentials file as `credentials.json` in the project directory

## Usage

### Basic Usage

List available sites:
```bash
python analyze.py
```

Analyze a specific site:
```bash
python analyze.py --site https://www.example.com
```

### Advanced Options

```bash
python analyze.py \
  --site https://www.example.com \
  --days 90 \
  --credentials my_credentials.json \
  --output my_reports \
  --no-viz
```

### Parameters

- `--site`: Site URL to analyze (required for analysis)
- `--days`: Number of days of data to analyze (default: 30)
- `--credentials`: Path to Google OAuth credentials file (default: credentials.json)
- `--output`: Output directory for reports (default: output)
- `--no-viz`: Skip visualization generation

## Output

The tool generates several output files in the specified output directory:

### 1. `detailed_analysis.csv`
Complete dataset with all analyzed queries including:
- Query text and metrics (clicks, impressions, CTR, position)
- Sentiment scores and classification
- Intent classification
- Extracted entities and key phrases
- Query characteristics

### 2. `analysis_summary.json`
Structured JSON containing:
- Sentiment distribution and performance
- Intent distribution and performance
- Entity analysis results
- Identified strengths and weaknesses
- Optimization opportunities
- AI citation strategy recommendations

### 3. `analysis_report.txt`
Human-readable text report with:
- Executive summary
- Sentiment and intent breakdowns
- Top strengths and weaknesses
- Actionable opportunities
- Top AI citation opportunities

### 4. Visualizations (PNG files)
- `sentiment_distribution.png`: Pie chart of sentiment breakdown
- `intent_distribution.png`: Bar chart of search intent
- `performance_by_sentiment.png`: Multi-panel performance comparison
- `top_entities.png`: Top entities by traffic
- `ctr_vs_position.png`: Scatter plot showing CTR and position relationship
- `query_length_distribution.png`: Distribution of query lengths

## Understanding the Results

### Sentiment Categories

- **Positive**: Queries with positive keywords (best, top, great) or positive polarity
- **Negative**: Queries with problem/issue keywords or negative polarity
- **Neutral**: Queries without strong sentiment indicators

### Intent Categories

- **Informational**: Questions and knowledge-seeking queries
- **Commercial**: Buying-intent, comparisons, reviews
- **Problem-Solving**: Troubleshooting, fixes, solutions
- **Navigational**: Brand names, direct navigation

### AI Citation Opportunities

The tool identifies entities that:
- Drive significant traffic
- Have good rankings (position < 10)
- Are of types favored by AI models (PERSON, ORG, PRODUCT, etc.)
- Present opportunities for structured data markup

## Use Cases

### 1. Content Strategy
- Identify which content types perform best
- Discover gaps in coverage (low commercial intent traffic)
- Find opportunities for new content

### 2. SEO Optimization
- Understand what's working (strengths)
- Fix underperforming areas (weaknesses)
- Prioritize optimization efforts

### 3. AI Search Readiness
- Identify entities to emphasize
- Get structured data recommendations
- Build authority for AI citations

### 4. User Intent Understanding
- See what problems users are trying to solve
- Understand buying journey stages
- Align content with user needs

## Theoretical Background

This tool is based on insights from sentiment analysis and entity-based SEO research, incorporating:

1. **Natural Language Processing**: Using TextBlob and spaCy for sentiment and entity extraction
2. **Search Intent Classification**: Categorizing queries based on keyword patterns and structure
3. **Entity-Based SEO**: Focusing on entities that search engines and AI models recognize
4. **E-E-A-T Principles**: Emphasizing expertise, experience, authoritativeness, and trustworthiness
5. **AI Citation Optimization**: Preparing content for AI-powered search features

## Troubleshooting

### "Credentials file not found"
Make sure you've downloaded the OAuth credentials from Google Cloud Console and saved them as `credentials.json`.

### "No data found"
- Ensure the site URL is correct and includes the protocol (https://)
- Verify you have access to this site in Google Search Console
- Try a longer time period with `--days 90`
- Check that your site has recent search traffic

### "Model not found" (spaCy)
Install the English model:
```bash
python -m spacy download en_core_web_sm
```

### API Rate Limits
The tool respects Google's API rate limits. If you hit limits, try:
- Reducing the time period (--days)
- Waiting a few minutes before retrying

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

MIT License - feel free to use this tool for personal or commercial projects.

## Author

Developed with insights from sentiment analysis and entity-based SEO research.

## Acknowledgments

- Google Search Console API
- TextBlob for sentiment analysis
- spaCy for entity extraction
- The SEO and data science communities