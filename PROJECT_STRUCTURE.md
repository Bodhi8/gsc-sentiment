# Project Structure

```
gsc-sentiment/
├── README.md                      # Main documentation
├── QUICKSTART.md                  # Quick start guide
├── GUIDE.md                       # Detailed usage guide and theory
├── LICENSE                        # MIT License
│
├── requirements.txt               # Python dependencies
├── setup.sh                       # Unix/Linux/Mac setup script
├── setup.bat                      # Windows setup script
├── .gitignore                     # Git ignore rules
│
├── config.example.json            # Example configuration
│
├── Core Modules
│   ├── gsc_connector.py          # Google Search Console API integration
│   ├── sentiment_analyzer.py    # Sentiment and intent analysis
│   ├── entity_analyzer.py       # Entity extraction and AI citations
│   ├── insights_generator.py    # Insights and recommendations
│   └── visualizations.py        # Chart and graph generation
│
├── Main Tools
│   ├── analyze.py               # CLI analysis tool
│   └── analysis_notebook.ipynb # Jupyter notebook for interactive analysis
│
└── Testing
    └── test_modules.py          # Test suite for core modules
```

## File Descriptions

### Documentation Files

- **README.md**: Complete project documentation with installation, usage, and examples
- **QUICKSTART.md**: Step-by-step setup guide for beginners
- **GUIDE.md**: In-depth guide covering theory, use cases, and best practices
- **LICENSE**: MIT License for open-source use

### Configuration Files

- **requirements.txt**: All Python package dependencies
- **config.example.json**: Template for custom configuration
- **.gitignore**: Files to exclude from version control

### Setup Scripts

- **setup.sh**: Automated setup for Unix/Linux/Mac systems
- **setup.bat**: Automated setup for Windows systems

### Core Python Modules

- **gsc_connector.py**: Handles authentication and data retrieval from Google Search Console API
- **sentiment_analyzer.py**: Analyzes sentiment and classifies search intent using TextBlob
- **entity_analyzer.py**: Extracts entities with spaCy and identifies AI citation opportunities
- **insights_generator.py**: Generates actionable insights, strengths, weaknesses, and strategies
- **visualizations.py**: Creates charts and graphs using matplotlib and seaborn

### User-Facing Tools

- **analyze.py**: Command-line tool for running complete analysis
- **analysis_notebook.ipynb**: Jupyter notebook for interactive exploration and custom analysis

### Testing

- **test_modules.py**: Unit and integration tests for all core modules

## Module Dependencies

```
analyze.py
  ├── gsc_connector.py
  ├── sentiment_analyzer.py
  ├── entity_analyzer.py
  ├── insights_generator.py
  └── visualizations.py

sentiment_analyzer.py
  └── textblob

entity_analyzer.py
  └── spacy

insights_generator.py
  ├── sentiment_analyzer
  └── entity_analyzer

visualizations.py
  ├── matplotlib
  ├── seaborn
  └── plotly
```

## Data Flow

```
1. Google Search Console
        ↓
2. gsc_connector.py (Fetch data)
        ↓
3. sentiment_analyzer.py (Analyze sentiment & intent)
        ↓
4. entity_analyzer.py (Extract entities)
        ↓
5. insights_generator.py (Generate insights)
        ↓
6. visualizations.py (Create charts)
        ↓
7. Output Files
   ├── detailed_analysis.csv
   ├── analysis_summary.json
   ├── analysis_report.txt
   └── *.png (visualizations)
```

## Output Structure

When you run the analysis, it creates an output directory:

```
output/
├── detailed_analysis.csv           # Complete query-level data
├── analysis_summary.json           # Structured summary data
├── analysis_report.txt            # Human-readable report
├── sentiment_distribution.png     # Sentiment pie chart
├── intent_distribution.png        # Intent bar chart
├── performance_by_sentiment.png   # Multi-panel performance charts
├── top_entities.png              # Top entities by traffic
├── ctr_vs_position.png           # CTR vs position scatter plot
└── query_length_distribution.png  # Query length histogram
```
