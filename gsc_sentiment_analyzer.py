"""
Google Search Console Sentiment Analysis Tool

This module provides functionality to analyze sentiment from Google Search Console data,
identifying site strengths, weaknesses, and entities that contribute to AI citations.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from google.oauth2 import service_account
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import spacy
from collections import Counter
import warnings
warnings.filterwarnings('ignore')


class GSCSentimentAnalyzer:
    """Analyzes sentiment and entities from Google Search Console data."""
    
    def __init__(self, credentials_path: str, site_url: str):
        """
        Initialize the GSC Sentiment Analyzer.
        
        Args:
            credentials_path: Path to Google Cloud service account credentials
            site_url: The Search Console property URL
        """
        self.site_url = site_url
        self.credentials_path = credentials_path
        self.service = self._authenticate()
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Try to load spaCy model, fallback if not available
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model 'en_core_web_sm' not found.")
            print("Entity extraction will be limited. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def _authenticate(self):
        """Authenticate with Google Search Console API."""
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_path,
            scopes=['https://www.googleapis.com/auth/webmasters.readonly']
        )
        return build('searchconsole', 'v1', credentials=credentials)
    
    def fetch_search_analytics(
        self,
        start_date: str,
        end_date: str,
        dimensions: List[str] = ['query', 'page'],
        max_rows: int = 25000
    ) -> pd.DataFrame:
        """
        Fetch search analytics data from Google Search Console.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            dimensions: Dimensions to query (e.g., 'query', 'page', 'country', 'device')
            max_rows: Maximum number of rows to fetch
            
        Returns:
            DataFrame with search analytics data
        """
        request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': dimensions,
            'rowLimit': max_rows,
            'startRow': 0
        }
        
        response = self.service.searchanalytics().query(
            siteUrl=self.site_url,
            body=request
        ).execute()
        
        if 'rows' not in response:
            print("No data available for the specified date range.")
            return pd.DataFrame()
        
        # Parse response into DataFrame
        rows = []
        for row in response['rows']:
            data = {
                'clicks': row['clicks'],
                'impressions': row['impressions'],
                'ctr': row['ctr'],
                'position': row['position']
            }
            
            # Add dimension values
            for i, dimension in enumerate(dimensions):
                data[dimension] = row['keys'][i]
            
            rows.append(data)
        
        df = pd.DataFrame(rows)
        return df
    
    def analyze_query_sentiment(self, query: str) -> Dict[str, float]:
        """
        Analyze sentiment of a search query using multiple methods.
        
        Args:
            query: Search query text
            
        Returns:
            Dictionary with sentiment scores from different analyzers
        """
        # VADER sentiment (good for social media and web content)
        vader_scores = self.vader_analyzer.polarity_scores(query)
        
        # TextBlob sentiment
        blob = TextBlob(query)
        textblob_polarity = blob.sentiment.polarity
        textblob_subjectivity = blob.sentiment.subjectivity
        
        return {
            'vader_compound': vader_scores['compound'],
            'vader_positive': vader_scores['pos'],
            'vader_negative': vader_scores['neg'],
            'vader_neutral': vader_scores['neu'],
            'textblob_polarity': textblob_polarity,
            'textblob_subjectivity': textblob_subjectivity
        }
    
    def extract_entities(self, text: str) -> List[Tuple[str, str]]:
        """
        Extract named entities from text.
        
        Args:
            text: Input text
            
        Returns:
            List of (entity_text, entity_type) tuples
        """
        if self.nlp is None:
            return []
        
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities
    
    def analyze_dataframe(
        self,
        df: pd.DataFrame,
        min_impressions: int = 10
    ) -> pd.DataFrame:
        """
        Add sentiment analysis to the GSC data.
        
        Args:
            df: DataFrame with GSC data
            min_impressions: Minimum impressions to include in analysis
            
        Returns:
            DataFrame with added sentiment columns
        """
        # Filter by minimum impressions
        df = df[df['impressions'] >= min_impressions].copy()
        
        if df.empty:
            print("No data meets the minimum impressions criteria.")
            return df
        
        # Analyze sentiment for each query
        print(f"Analyzing sentiment for {len(df)} queries...")
        sentiment_data = []
        
        for query in df['query'].unique():
            sentiment = self.analyze_query_sentiment(query)
            sentiment['query'] = query
            sentiment_data.append(sentiment)
        
        sentiment_df = pd.DataFrame(sentiment_data)
        
        # Merge sentiment data with original data
        df = df.merge(sentiment_df, on='query', how='left')
        
        return df
    
    def categorize_sentiment(self, compound_score: float) -> str:
        """
        Categorize sentiment based on VADER compound score.
        
        Args:
            compound_score: VADER compound score (-1 to 1)
            
        Returns:
            Sentiment category
        """
        if compound_score >= 0.05:
            return 'positive'
        elif compound_score <= -0.05:
            return 'negative'
        else:
            return 'neutral'
    
    def identify_strengths_weaknesses(
        self,
        df: pd.DataFrame
    ) -> Dict[str, pd.DataFrame]:
        """
        Identify site strengths and weaknesses based on sentiment and performance.
        
        Args:
            df: DataFrame with sentiment analysis
            
        Returns:
            Dictionary with strengths and weaknesses DataFrames
        """
        # Add sentiment category
        df['sentiment_category'] = df['vader_compound'].apply(self.categorize_sentiment)
        
        # Calculate performance score (weighted combination of metrics)
        df['performance_score'] = (
            df['clicks'] * 0.4 +
            df['impressions'] * 0.1 +
            df['ctr'] * 100 * 0.3 +
            (100 - df['position']) * 0.2
        )
        
        # Normalize performance score
        if df['performance_score'].max() > 0:
            df['performance_score'] = (
                df['performance_score'] / df['performance_score'].max() * 100
            )
        
        # Strengths: High performance + positive sentiment
        strengths = df[
            (df['performance_score'] >= df['performance_score'].quantile(0.75)) &
            (df['vader_compound'] >= 0.05)
        ].sort_values('performance_score', ascending=False)
        
        # Weaknesses: Low performance or negative sentiment
        weaknesses = df[
            (df['performance_score'] <= df['performance_score'].quantile(0.25)) |
            (df['vader_compound'] <= -0.05)
        ].sort_values('performance_score')
        
        return {
            'strengths': strengths,
            'weaknesses': weaknesses,
            'all_data': df
        }
    
    def analyze_entities_for_citations(
        self,
        df: pd.DataFrame,
        top_n: int = 50
    ) -> Dict[str, any]:
        """
        Analyze entities that contribute to potential AI citations.
        
        Args:
            df: DataFrame with GSC data
            top_n: Number of top queries to analyze for entities
            
        Returns:
            Dictionary with entity analysis results
        """
        # Get top performing queries
        top_queries = df.nlargest(top_n, 'clicks')['query'].tolist()
        
        # Extract entities from top queries
        all_entities = []
        entity_query_map = {}
        
        for query in top_queries:
            entities = self.extract_entities(query)
            for entity_text, entity_type in entities:
                all_entities.append({
                    'entity': entity_text,
                    'type': entity_type,
                    'query': query
                })
                
                if entity_text not in entity_query_map:
                    entity_query_map[entity_text] = []
                entity_query_map[entity_text].append(query)
        
        if not all_entities:
            return {
                'entities': pd.DataFrame(),
                'entity_types': {},
                'top_entities': []
            }
        
        entities_df = pd.DataFrame(all_entities)
        
        # Count entity occurrences
        entity_counts = entities_df['entity'].value_counts().to_dict()
        entity_type_counts = entities_df['type'].value_counts().to_dict()
        
        # Get top entities with their associated queries
        top_entities = []
        for entity, count in list(entity_counts.items())[:20]:
            queries = entity_query_map[entity]
            entity_type = entities_df[entities_df['entity'] == entity]['type'].iloc[0]
            
            top_entities.append({
                'entity': entity,
                'type': entity_type,
                'frequency': count,
                'sample_queries': queries[:5]
            })
        
        return {
            'entities': entities_df,
            'entity_types': entity_type_counts,
            'top_entities': top_entities
        }
    
    def generate_insights(
        self,
        analysis_results: Dict[str, any]
    ) -> str:
        """
        Generate human-readable insights from analysis results.
        
        Args:
            analysis_results: Dictionary with all analysis results
            
        Returns:
            Formatted insights report
        """
        df = analysis_results['all_data']
        strengths = analysis_results['strengths']
        weaknesses = analysis_results['weaknesses']
        
        insights = []
        insights.append("=" * 80)
        insights.append("GOOGLE SEARCH CONSOLE SENTIMENT ANALYSIS REPORT")
        insights.append("=" * 80)
        insights.append("")
        
        # Overall statistics
        insights.append("OVERALL STATISTICS")
        insights.append("-" * 80)
        insights.append(f"Total queries analyzed: {len(df)}")
        insights.append(f"Total clicks: {df['clicks'].sum():,.0f}")
        insights.append(f"Total impressions: {df['impressions'].sum():,.0f}")
        insights.append(f"Average CTR: {df['ctr'].mean():.2%}")
        insights.append(f"Average position: {df['position'].mean():.1f}")
        insights.append("")
        
        # Sentiment distribution
        sentiment_dist = df['sentiment_category'].value_counts()
        insights.append("SENTIMENT DISTRIBUTION")
        insights.append("-" * 80)
        for sentiment, count in sentiment_dist.items():
            percentage = count / len(df) * 100
            insights.append(f"{sentiment.capitalize()}: {count} ({percentage:.1f}%)")
        insights.append("")
        
        # Average sentiment score
        avg_sentiment = df['vader_compound'].mean()
        insights.append(f"Average sentiment score: {avg_sentiment:.3f}")
        insights.append("")
        
        # Strengths
        insights.append("TOP STRENGTHS (High Performance + Positive Sentiment)")
        insights.append("-" * 80)
        if len(strengths) > 0:
            for idx, row in strengths.head(10).iterrows():
                insights.append(f"\nQuery: {row['query']}")
                insights.append(f"  - Clicks: {row['clicks']:.0f} | Impressions: {row['impressions']:.0f}")
                insights.append(f"  - CTR: {row['ctr']:.2%} | Position: {row['position']:.1f}")
                insights.append(f"  - Sentiment: {row['vader_compound']:.3f} ({row['sentiment_category']})")
                insights.append(f"  - Performance Score: {row['performance_score']:.1f}/100")
        else:
            insights.append("No strong performers identified.")
        insights.append("")
        
        # Weaknesses
        insights.append("TOP WEAKNESSES (Low Performance or Negative Sentiment)")
        insights.append("-" * 80)
        if len(weaknesses) > 0:
            for idx, row in weaknesses.head(10).iterrows():
                insights.append(f"\nQuery: {row['query']}")
                insights.append(f"  - Clicks: {row['clicks']:.0f} | Impressions: {row['impressions']:.0f}")
                insights.append(f"  - CTR: {row['ctr']:.2%} | Position: {row['position']:.1f}")
                insights.append(f"  - Sentiment: {row['vader_compound']:.3f} ({row['sentiment_category']})")
                insights.append(f"  - Performance Score: {row['performance_score']:.1f}/100")
        else:
            insights.append("No significant weaknesses identified.")
        insights.append("")
        
        # Entity analysis
        if 'entity_analysis' in analysis_results:
            entity_results = analysis_results['entity_analysis']
            insights.append("ENTITY ANALYSIS FOR AI CITATIONS")
            insights.append("-" * 80)
            
            if entity_results['top_entities']:
                insights.append("Top entities mentioned in high-performing queries:")
                for entity_info in entity_results['top_entities'][:15]:
                    insights.append(f"\n  {entity_info['entity']} ({entity_info['type']})")
                    insights.append(f"    - Frequency: {entity_info['frequency']}")
                    insights.append(f"    - Sample queries: {', '.join(entity_info['sample_queries'][:3])}")
            else:
                insights.append("No entities extracted. Ensure spaCy model is installed.")
            
            insights.append("")
            
            if entity_results['entity_types']:
                insights.append("Entity types distribution:")
                for entity_type, count in entity_results['entity_types'].items():
                    insights.append(f"  - {entity_type}: {count}")
        
        insights.append("")
        insights.append("=" * 80)
        insights.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        insights.append("=" * 80)
        
        return "\n".join(insights)
    
    def save_results(
        self,
        analysis_results: Dict[str, any],
        output_dir: str = 'outputs'
    ):
        """
        Save analysis results to CSV files.
        
        Args:
            analysis_results: Dictionary with all analysis results
            output_dir: Directory to save output files
        """
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save full data
        analysis_results['all_data'].to_csv(
            f"{output_dir}/full_analysis_{timestamp}.csv",
            index=False
        )
        
        # Save strengths
        analysis_results['strengths'].to_csv(
            f"{output_dir}/strengths_{timestamp}.csv",
            index=False
        )
        
        # Save weaknesses
        analysis_results['weaknesses'].to_csv(
            f"{output_dir}/weaknesses_{timestamp}.csv",
            index=False
        )
        
        # Save insights report
        insights = self.generate_insights(analysis_results)
        with open(f"{output_dir}/insights_report_{timestamp}.txt", 'w') as f:
            f.write(insights)
        
        print(f"\nResults saved to {output_dir}/")
        print(f"  - full_analysis_{timestamp}.csv")
        print(f"  - strengths_{timestamp}.csv")
        print(f"  - weaknesses_{timestamp}.csv")
        print(f"  - insights_report_{timestamp}.txt")


def main():
    """Example usage of the GSC Sentiment Analyzer."""
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Configuration
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    site_url = os.getenv('SITE_URL')
    start_date = os.getenv('START_DATE', '2024-01-01')
    end_date = os.getenv('END_DATE', '2024-12-31')
    max_rows = int(os.getenv('MAX_ROWS', 25000))
    min_impressions = int(os.getenv('MIN_IMPRESSIONS', 10))
    
    if not credentials_path or not site_url:
        print("Error: Missing required environment variables.")
        print("Please set GOOGLE_APPLICATION_CREDENTIALS and SITE_URL in .env file")
        return
    
    # Initialize analyzer
    print("Initializing GSC Sentiment Analyzer...")
    analyzer = GSCSentimentAnalyzer(credentials_path, site_url)
    
    # Fetch data
    print(f"\nFetching data from {start_date} to {end_date}...")
    df = analyzer.fetch_search_analytics(
        start_date=start_date,
        end_date=end_date,
        dimensions=['query', 'page'],
        max_rows=max_rows
    )
    
    if df.empty:
        print("No data available.")
        return
    
    print(f"Fetched {len(df)} rows of data.")
    
    # Analyze sentiment
    print("\nPerforming sentiment analysis...")
    df_analyzed = analyzer.analyze_dataframe(df, min_impressions=min_impressions)
    
    # Identify strengths and weaknesses
    print("\nIdentifying strengths and weaknesses...")
    analysis_results = analyzer.identify_strengths_weaknesses(df_analyzed)
    
    # Analyze entities
    print("\nAnalyzing entities for AI citations...")
    entity_analysis = analyzer.analyze_entities_for_citations(df_analyzed, top_n=100)
    analysis_results['entity_analysis'] = entity_analysis
    
    # Generate and print insights
    print("\n" + analyzer.generate_insights(analysis_results))
    
    # Save results
    analyzer.save_results(analysis_results)


if __name__ == '__main__':
    main()
