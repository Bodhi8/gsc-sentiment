# API Reference

## GSCSentimentAnalyzer

Main class for analyzing sentiment from Google Search Console data.

### Constructor

```python
GSCSentimentAnalyzer(credentials_path: str, site_url: str)
```

**Parameters:**
- `credentials_path` (str): Path to Google Cloud service account credentials JSON file
- `site_url` (str): The Search Console property URL (e.g., "https://example.com")

**Example:**
```python
analyzer = GSCSentimentAnalyzer(
    credentials_path='credentials.json',
    site_url='https://example.com'
)
```

---

### Methods

#### fetch_search_analytics

Fetch search analytics data from Google Search Console.

```python
fetch_search_analytics(
    start_date: str,
    end_date: str,
    dimensions: List[str] = ['query', 'page'],
    max_rows: int = 25000
) -> pd.DataFrame
```

**Parameters:**
- `start_date` (str): Start date in YYYY-MM-DD format
- `end_date` (str): End date in YYYY-MM-DD format
- `dimensions` (List[str]): Dimensions to query. Options: 'query', 'page', 'country', 'device', 'searchAppearance'
- `max_rows` (int): Maximum number of rows to fetch (default: 25000)

**Returns:**
- `pd.DataFrame`: DataFrame with search analytics data

**Example:**
```python
df = analyzer.fetch_search_analytics(
    start_date='2024-01-01',
    end_date='2024-12-31',
    dimensions=['query', 'page', 'country'],
    max_rows=10000
)
```

---

#### analyze_query_sentiment

Analyze sentiment of a single search query.

```python
analyze_query_sentiment(query: str) -> Dict[str, float]
```

**Parameters:**
- `query` (str): Search query text

**Returns:**
- `Dict[str, float]`: Dictionary with sentiment scores:
  - `vader_compound`: Overall sentiment (-1 to 1)
  - `vader_positive`: Positive score (0 to 1)
  - `vader_negative`: Negative score (0 to 1)
  - `vader_neutral`: Neutral score (0 to 1)
  - `textblob_polarity`: Polarity (-1 to 1)
  - `textblob_subjectivity`: Subjectivity (0 to 1)

**Example:**
```python
sentiment = analyzer.analyze_query_sentiment("best python tutorial")
print(f"Sentiment: {sentiment['vader_compound']:.3f}")
```

---

#### extract_entities

Extract named entities from text using spaCy.

```python
extract_entities(text: str) -> List[Tuple[str, str]]
```

**Parameters:**
- `text` (str): Input text

**Returns:**
- `List[Tuple[str, str]]`: List of (entity_text, entity_type) tuples

**Entity Types:**
- PERSON: People, including fictional
- ORG: Companies, agencies, institutions
- GPE: Countries, cities, states
- PRODUCT: Objects, vehicles, foods, etc.
- EVENT: Named events
- WORK_OF_ART: Titles of books, songs, etc.
- And more...

**Example:**
```python
entities = analyzer.extract_entities("Python tutorial by Google")
# Returns: [('Python', 'PRODUCT'), ('Google', 'ORG')]
```

---

#### analyze_dataframe

Add sentiment analysis to the entire GSC DataFrame.

```python
analyze_dataframe(
    df: pd.DataFrame,
    min_impressions: int = 10
) -> pd.DataFrame
```

**Parameters:**
- `df` (pd.DataFrame): DataFrame with GSC data
- `min_impressions` (int): Minimum impressions to include in analysis

**Returns:**
- `pd.DataFrame`: DataFrame with added sentiment columns

**Example:**
```python
df_analyzed = analyzer.analyze_dataframe(df, min_impressions=5)
```

---

#### identify_strengths_weaknesses

Identify site strengths and weaknesses based on sentiment and performance.

```python
identify_strengths_weaknesses(
    df: pd.DataFrame
) -> Dict[str, pd.DataFrame]
```

**Parameters:**
- `df` (pd.DataFrame): DataFrame with sentiment analysis

**Returns:**
- `Dict[str, pd.DataFrame]`: Dictionary containing:
  - `strengths`: High-performing queries with positive sentiment
  - `weaknesses`: Low-performing queries or negative sentiment
  - `all_data`: Complete dataset with performance scores

**Example:**
```python
results = analyzer.identify_strengths_weaknesses(df_analyzed)
print(f"Strengths: {len(results['strengths'])}")
print(f"Weaknesses: {len(results['weaknesses'])}")
```

---

#### analyze_entities_for_citations

Analyze entities that contribute to potential AI citations.

```python
analyze_entities_for_citations(
    df: pd.DataFrame,
    top_n: int = 50
) -> Dict[str, any]
```

**Parameters:**
- `df` (pd.DataFrame): DataFrame with GSC data
- `top_n` (int): Number of top queries to analyze for entities

**Returns:**
- `Dict[str, any]`: Dictionary with:
  - `entities`: DataFrame with all entities
  - `entity_types`: Count of entity types
  - `top_entities`: List of top entities with details

**Example:**
```python
entity_analysis = analyzer.analyze_entities_for_citations(df, top_n=100)
for entity in entity_analysis['top_entities'][:10]:
    print(f"{entity['entity']}: {entity['frequency']} occurrences")
```

---

#### generate_insights

Generate human-readable insights report.

```python
generate_insights(
    analysis_results: Dict[str, any]
) -> str
```

**Parameters:**
- `analysis_results` (Dict): Dictionary with all analysis results

**Returns:**
- `str`: Formatted insights report

**Example:**
```python
insights = analyzer.generate_insights(results)
print(insights)
```

---

#### save_results

Save analysis results to CSV files.

```python
save_results(
    analysis_results: Dict[str, any],
    output_dir: str = 'outputs'
)
```

**Parameters:**
- `analysis_results` (Dict): Dictionary with all analysis results
- `output_dir` (str): Directory to save output files

**Example:**
```python
analyzer.save_results(results, output_dir='outputs/my_analysis')
```

---

## SentimentVisualizer

Class for creating visualizations of sentiment analysis results.

### Constructor

```python
SentimentVisualizer(style: str = 'seaborn-v0_8-darkgrid')
```

**Parameters:**
- `style` (str): Matplotlib style to use

---

### Methods

#### plot_sentiment_distribution

Plot sentiment distribution pie chart.

```python
plot_sentiment_distribution(
    df: pd.DataFrame,
    output_path: Optional[str] = None
)
```

**Parameters:**
- `df` (pd.DataFrame): DataFrame with sentiment_category column
- `output_path` (str, optional): Path to save the plot

---

#### plot_sentiment_vs_performance

Plot sentiment score vs performance metrics.

```python
plot_sentiment_vs_performance(
    df: pd.DataFrame,
    output_path: Optional[str] = None
)
```

**Parameters:**
- `df` (pd.DataFrame): DataFrame with sentiment and performance data
- `output_path` (str, optional): Path to save the plot

---

#### plot_top_performers

Plot top strengths and weaknesses.

```python
plot_top_performers(
    strengths_df: pd.DataFrame,
    weaknesses_df: pd.DataFrame,
    top_n: int = 10,
    output_path: Optional[str] = None
)
```

**Parameters:**
- `strengths_df` (pd.DataFrame): DataFrame with strengths
- `weaknesses_df` (pd.DataFrame): DataFrame with weaknesses
- `top_n` (int): Number of top items to show
- `output_path` (str, optional): Path to save the plot

---

#### plot_entity_analysis

Plot entity analysis results.

```python
plot_entity_analysis(
    entity_analysis: Dict,
    top_n: int = 15,
    output_path: Optional[str] = None
)
```

**Parameters:**
- `entity_analysis` (Dict): Dictionary with entity analysis results
- `top_n` (int): Number of top entities to show
- `output_path` (str, optional): Path to save the plot

---

#### create_interactive_dashboard

Create an interactive Plotly dashboard.

```python
create_interactive_dashboard(
    df: pd.DataFrame,
    output_path: str = 'outputs/interactive_dashboard.html'
)
```

**Parameters:**
- `df` (pd.DataFrame): DataFrame with analysis results
- `output_path` (str): Path to save the HTML dashboard

---

#### generate_all_visualizations

Generate all visualizations at once.

```python
generate_all_visualizations(
    analysis_results: Dict,
    output_dir: str = 'outputs'
)
```

**Parameters:**
- `analysis_results` (Dict): Dictionary with all analysis results
- `output_dir` (str): Directory to save visualizations

**Example:**
```python
visualizer = SentimentVisualizer()
visualizer.generate_all_visualizations(results, output_dir='outputs')
```

---

## Data Structures

### GSC Data DataFrame Columns

After `fetch_search_analytics`:
- `query` (str): Search query
- `page` (str): Landing page URL
- `clicks` (int): Number of clicks
- `impressions` (int): Number of impressions
- `ctr` (float): Click-through rate (0-1)
- `position` (float): Average position in search results

Optional dimensions:
- `country` (str): Country code (if included in dimensions)
- `device` (str): Device type (if included in dimensions)

### Analyzed DataFrame Columns

After `analyze_dataframe`, adds:
- `vader_compound` (float): Overall sentiment score (-1 to 1)
- `vader_positive` (float): Positive score (0 to 1)
- `vader_negative` (float): Negative score (0 to 1)
- `vader_neutral` (float): Neutral score (0 to 1)
- `textblob_polarity` (float): Polarity (-1 to 1)
- `textblob_subjectivity` (float): Subjectivity (0 to 1)

After `identify_strengths_weaknesses`, adds:
- `sentiment_category` (str): 'positive', 'neutral', or 'negative'
- `performance_score` (float): Normalized performance score (0-100)

---

## Complete Usage Example

```python
from gsc_sentiment_analyzer import GSCSentimentAnalyzer
from visualizations import SentimentVisualizer

# Initialize
analyzer = GSCSentimentAnalyzer(
    credentials_path='credentials.json',
    site_url='https://example.com'
)

# Fetch data
df = analyzer.fetch_search_analytics(
    start_date='2024-01-01',
    end_date='2024-12-31',
    dimensions=['query', 'page'],
    max_rows=25000
)

# Analyze
df_analyzed = analyzer.analyze_dataframe(df, min_impressions=10)
results = analyzer.identify_strengths_weaknesses(df_analyzed)
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
