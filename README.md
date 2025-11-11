# Google Search Console Sentiment Analysis

A comprehensive tool for analyzing sentiment from Google Search Console data to identify site strengths, weaknesses, and entities that contribute to AI citations.

## Features

- **Sentiment Analysis**: Analyze search queries using VADER and TextBlob sentiment analyzers
- **Performance Metrics**: Combine sentiment with GSC performance data (clicks, impressions, CTR, position)
- **Strengths & Weaknesses**: Automatically identify high-performing and underperforming content
- **Entity Extraction**: Extract and analyze named entities that appear in top queries (important for AI citations)
- **Comprehensive Reporting**: Generate detailed text reports and CSV exports
- **Rich Visualizations**: Create static and interactive visualizations of your data

## Inspired by Medium Articles

This tool implements sentiment analysis concepts for Search Console data as discussed in articles on understanding:
- Where sites are weak and strong in terms of sentiment and performance
- Which entities help with AI citations and visibility
- How to leverage search data for content strategy

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account with Search Console API enabled
- Google Search Console property with data

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Bodhi8/gsc-sentiment.git
cd gsc-sentiment
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download the spaCy language model for entity extraction:
```bash
python -m spacy download en_core_web_sm
```

### Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Search Console API
4. Create a service account:
   - Go to IAM & Admin > Service Accounts
   - Create a new service account
   - Download the JSON credentials file
5. Add the service account email to your Search Console property:
   - Go to [Google Search Console](https://search.google.com/search-console)
   - Select your property
   - Go to Settings > Users and permissions
   - Add the service account email as a user with "Full" permissions

### Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and update the following:
```
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
SITE_URL=https://yourdomain.com
START_DATE=2024-01-01
END_DATE=2024-12-31
MAX_ROWS=25000
MIN_IMPRESSIONS=10
```

## Usage

### Basic Usage

Run the sentiment analysis:
```bash
python gsc_sentiment_analyzer.py
```

This will:
1. Fetch data from Google Search Console
2. Perform sentiment analysis on all queries
3. Identify strengths and weaknesses
4. Extract entities for AI citation analysis
5. Generate reports and save results to the `outputs/` directory

### Advanced Usage

#### Using as a Python Module

```python
from gsc_sentiment_analyzer import GSCSentimentAnalyzer
from visualizations import SentimentVisualizer

# Initialize
analyzer = GSCSentimentAnalyzer(
    credentials_path='path/to/credentials.json',
    site_url='https://yourdomain.com'
)

# Fetch data
df = analyzer.fetch_search_analytics(
    start_date='2024-01-01',
    end_date='2024-12-31',
    dimensions=['query', 'page'],
    max_rows=25000
)

# Analyze sentiment
df_analyzed = analyzer.analyze_dataframe(df, min_impressions=10)

# Identify strengths and weaknesses
results = analyzer.identify_strengths_weaknesses(df_analyzed)

# Analyze entities
entity_analysis = analyzer.analyze_entities_for_citations(df_analyzed, top_n=100)
results['entity_analysis'] = entity_analysis

# Generate insights
insights = analyzer.generate_insights(results)
print(insights)

# Save results
analyzer.save_results(results)

# Create visualizations
visualizer = SentimentVisualizer()
visualizer.generate_all_visualizations(results)
```

#### Custom Analysis

```python
# Analyze specific date range
df = analyzer.fetch_search_analytics(
    start_date='2024-06-01',
    end_date='2024-06-30',
    dimensions=['query', 'page', 'country'],
    max_rows=10000
)

# Filter for specific country
df_us = df[df['country'] == 'USA']

# Analyze sentiment
df_analyzed = analyzer.analyze_dataframe(df_us)
```

## Output Files

The tool generates several output files in the `outputs/` directory:

- `full_analysis_TIMESTAMP.csv`: Complete data with sentiment scores
- `strengths_TIMESTAMP.csv`: High-performing queries with positive sentiment
- `weaknesses_TIMESTAMP.csv`: Low-performing queries or negative sentiment
- `insights_report_TIMESTAMP.txt`: Detailed text report with insights
- `sentiment_distribution_TIMESTAMP.png`: Pie chart of sentiment categories
- `sentiment_vs_performance_TIMESTAMP.png`: Correlations between sentiment and metrics
- `top_performers_TIMESTAMP.png`: Bar charts of top strengths and weaknesses
- `entity_analysis_TIMESTAMP.png`: Entity frequency and type distribution
- `interactive_dashboard_TIMESTAMP.html`: Interactive Plotly dashboard

## Understanding the Results

### Sentiment Scores

- **VADER Compound Score** (-1 to 1):
  - Positive: >= 0.05
  - Neutral: -0.05 to 0.05
  - Negative: <= -0.05

- **TextBlob Polarity** (-1 to 1):
  - Measures sentiment polarity
  
- **TextBlob Subjectivity** (0 to 1):
  - 0 = very objective, 1 = very subjective

### Performance Score

Weighted combination of:
- Clicks (40%)
- Impressions (10%)
- CTR (30%)
- Position (20%)

Normalized to 0-100 scale.

### Strengths

Queries in the top 25% of performance scores with positive sentiment (compound >= 0.05).

### Weaknesses

Queries in the bottom 25% of performance scores OR with negative sentiment (compound <= -0.05).

### Entity Analysis

Identifies named entities (people, organizations, locations, etc.) in top-performing queries. These entities are important for:
- Understanding topic authority
- Identifying citation opportunities
- AI-driven search results (e.g., Google SGE, ChatGPT)

## Examples

### Example Report Output

```
================================================================================
GOOGLE SEARCH CONSOLE SENTIMENT ANALYSIS REPORT
================================================================================

OVERALL STATISTICS
--------------------------------------------------------------------------------
Total queries analyzed: 1,234
Total clicks: 45,678
Total impressions: 234,567
Average CTR: 19.47%
Average position: 12.3

SENTIMENT DISTRIBUTION
--------------------------------------------------------------------------------
Positive: 456 (37.0%)
Neutral: 678 (54.9%)
Negative: 100 (8.1%)

Average sentiment score: 0.125

TOP STRENGTHS (High Performance + Positive Sentiment)
--------------------------------------------------------------------------------
Query: best practices for python testing
  - Clicks: 234 | Impressions: 1,234
  - CTR: 18.96% | Position: 3.4
  - Sentiment: 0.765 (positive)
  - Performance Score: 87.3/100
...

TOP WEAKNESSES (Low Performance or Negative Sentiment)
--------------------------------------------------------------------------------
Query: python errors and bugs
  - Clicks: 2 | Impressions: 45
  - CTR: 4.44% | Position: 45.2
  - Sentiment: -0.543 (negative)
  - Performance Score: 12.1/100
...

ENTITY ANALYSIS FOR AI CITATIONS
--------------------------------------------------------------------------------
Top entities mentioned in high-performing queries:

  Python (LANGUAGE)
    - Frequency: 45
    - Sample queries: python testing, python best practices, python tutorial

  Django (PRODUCT)
    - Frequency: 23
    - Sample queries: django tutorial, django deployment, django vs flask
...
```

## Troubleshooting

### spaCy Model Not Found

If you see "spaCy model 'en_core_web_sm' not found", run:
```bash
python -m spacy download en_core_web_sm
```

### Authentication Errors

Ensure:
1. Service account JSON file path is correct in `.env`
2. Service account email is added to Search Console property
3. API is enabled in Google Cloud Console

### No Data Available

Check:
1. Date range is valid
2. Site URL matches exactly as shown in Search Console (with/without trailing slash)
3. Property has data for the specified date range

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Acknowledgments

Inspired by research and articles on:
- Sentiment analysis for SEO
- AI citations and entity optimization
- Search Console data analysis best practices

## Support

For issues and questions, please open an issue on GitHub.