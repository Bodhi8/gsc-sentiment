"""
Sentiment Analysis Module for Search Console Data

This module analyzes the sentiment of search queries and identifies
patterns that indicate user intent and emotional context.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from textblob import TextBlob
import re
from collections import Counter


class SentimentAnalyzer:
    """Analyze sentiment of search queries and content."""
    
    # Keywords indicating different sentiment categories
    POSITIVE_KEYWORDS = [
        'best', 'top', 'great', 'excellent', 'amazing', 'awesome', 'good',
        'love', 'favorite', 'recommended', 'perfect', 'beautiful', 'wonderful'
    ]
    
    NEGATIVE_KEYWORDS = [
        'worst', 'bad', 'terrible', 'poor', 'awful', 'hate', 'problem',
        'issue', 'error', 'fix', 'broken', 'not working', 'fail', 'wrong'
    ]
    
    QUESTION_KEYWORDS = [
        'how', 'what', 'why', 'when', 'where', 'who', 'which', 'can', 'is',
        'are', 'do', 'does', 'should', 'could', 'would'
    ]
    
    COMMERCIAL_KEYWORDS = [
        'buy', 'price', 'cost', 'cheap', 'discount', 'deal', 'sale',
        'review', 'compare', 'vs', 'versus', 'alternative'
    ]
    
    def __init__(self):
        """Initialize the sentiment analyzer."""
        self.sentiment_cache = {}
    
    def analyze_query_sentiment(self, query: str) -> Dict:
        """
        Analyze sentiment of a single search query.
        
        Args:
            query: The search query to analyze
            
        Returns:
            Dictionary with sentiment scores and classification
        """
        if query in self.sentiment_cache:
            return self.sentiment_cache[query]
        
        query_lower = query.lower()
        
        # TextBlob sentiment analysis
        blob = TextBlob(query)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Classify intent
        intent = self._classify_intent(query_lower)
        
        # Detect sentiment indicators
        has_positive = any(kw in query_lower for kw in self.POSITIVE_KEYWORDS)
        has_negative = any(kw in query_lower for kw in self.NEGATIVE_KEYWORDS)
        
        # Determine overall sentiment
        if has_negative or polarity < -0.1:
            sentiment = 'negative'
        elif has_positive or polarity > 0.1:
            sentiment = 'positive'
        else:
            sentiment = 'neutral'
        
        result = {
            'query': query,
            'polarity': polarity,
            'subjectivity': subjectivity,
            'sentiment': sentiment,
            'intent': intent,
            'has_positive_keywords': has_positive,
            'has_negative_keywords': has_negative,
            'query_length': len(query.split())
        }
        
        self.sentiment_cache[query] = result
        return result
    
    def _classify_intent(self, query: str) -> str:
        """
        Classify the search intent of a query.
        
        Args:
            query: Search query (lowercase)
            
        Returns:
            Intent classification
        """
        if any(kw in query for kw in self.QUESTION_KEYWORDS):
            return 'informational'
        elif any(kw in query for kw in self.COMMERCIAL_KEYWORDS):
            return 'commercial'
        elif any(kw in query for kw in self.NEGATIVE_KEYWORDS):
            return 'problem_solving'
        else:
            return 'navigational'
    
    def analyze_dataset(self, gsc_data: Dict) -> pd.DataFrame:
        """
        Analyze sentiment for entire GSC dataset.
        
        Args:
            gsc_data: GSC API response data
            
        Returns:
            DataFrame with sentiment analysis results
        """
        rows = gsc_data.get('rows', [])
        
        if not rows:
            return pd.DataFrame()
        
        analyzed_data = []
        
        for row in rows:
            keys = row.get('keys', [])
            query = keys[0] if keys else ''
            
            if not query:
                continue
            
            sentiment_result = self.analyze_query_sentiment(query)
            
            # Combine with GSC metrics
            data_point = {
                **sentiment_result,
                'clicks': row.get('clicks', 0),
                'impressions': row.get('impressions', 0),
                'ctr': row.get('ctr', 0),
                'position': row.get('position', 0)
            }
            
            if len(keys) > 1:
                data_point['page'] = keys[1]
            
            analyzed_data.append(data_point)
        
        df = pd.DataFrame(analyzed_data)
        return df
    
    def get_sentiment_summary(self, df: pd.DataFrame) -> Dict:
        """
        Generate summary statistics for sentiment analysis.
        
        Args:
            df: DataFrame with sentiment analysis
            
        Returns:
            Dictionary with summary statistics
        """
        if df.empty:
            return {}
        
        total_queries = len(df)
        total_clicks = df['clicks'].sum()
        total_impressions = df['impressions'].sum()
        
        sentiment_dist = df['sentiment'].value_counts().to_dict()
        intent_dist = df['intent'].value_counts().to_dict()
        
        # Performance by sentiment
        sentiment_performance = df.groupby('sentiment').agg({
            'clicks': 'sum',
            'impressions': 'sum',
            'ctr': 'mean',
            'position': 'mean'
        }).to_dict('index')
        
        # Performance by intent
        intent_performance = df.groupby('intent').agg({
            'clicks': 'sum',
            'impressions': 'sum',
            'ctr': 'mean',
            'position': 'mean'
        }).to_dict('index')
        
        return {
            'total_queries': total_queries,
            'total_clicks': total_clicks,
            'total_impressions': total_impressions,
            'avg_ctr': df['ctr'].mean(),
            'avg_position': df['position'].mean(),
            'sentiment_distribution': sentiment_dist,
            'intent_distribution': intent_dist,
            'performance_by_sentiment': sentiment_performance,
            'performance_by_intent': intent_performance,
            'avg_polarity': df['polarity'].mean(),
            'avg_subjectivity': df['subjectivity'].mean()
        }
