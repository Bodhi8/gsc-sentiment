"""
Unit tests for GSC Sentiment Analyzer
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gsc_sentiment_analyzer import GSCSentimentAnalyzer


class TestGSCSentimentAnalyzer(unittest.TestCase):
    """Test cases for GSCSentimentAnalyzer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock the authentication
        with patch('gsc_sentiment_analyzer.service_account.Credentials.from_service_account_file'):
            with patch('gsc_sentiment_analyzer.build'):
                self.analyzer = GSCSentimentAnalyzer(
                    credentials_path='fake_credentials.json',
                    site_url='https://example.com'
                )
    
    def test_analyze_query_sentiment_positive(self):
        """Test sentiment analysis for positive query"""
        query = "best python tutorial for beginners"
        result = self.analyzer.analyze_query_sentiment(query)
        
        self.assertIn('vader_compound', result)
        self.assertIn('vader_positive', result)
        self.assertIn('vader_negative', result)
        self.assertIn('vader_neutral', result)
        self.assertIn('textblob_polarity', result)
        self.assertIn('textblob_subjectivity', result)
        
        # Should be positive
        self.assertGreater(result['vader_compound'], 0)
    
    def test_analyze_query_sentiment_negative(self):
        """Test sentiment analysis for negative query"""
        query = "worst errors in python programming"
        result = self.analyzer.analyze_query_sentiment(query)
        
        # Should be negative
        self.assertLess(result['vader_compound'], 0)
    
    def test_analyze_query_sentiment_neutral(self):
        """Test sentiment analysis for neutral query"""
        query = "python programming language"
        result = self.analyzer.analyze_query_sentiment(query)
        
        # Should be relatively neutral
        self.assertGreaterEqual(result['vader_compound'], -0.5)
        self.assertLessEqual(result['vader_compound'], 0.5)
    
    def test_categorize_sentiment(self):
        """Test sentiment categorization"""
        self.assertEqual(self.analyzer.categorize_sentiment(0.5), 'positive')
        self.assertEqual(self.analyzer.categorize_sentiment(0.0), 'neutral')
        self.assertEqual(self.analyzer.categorize_sentiment(-0.5), 'negative')
        self.assertEqual(self.analyzer.categorize_sentiment(0.05), 'positive')
        self.assertEqual(self.analyzer.categorize_sentiment(-0.05), 'negative')
        self.assertEqual(self.analyzer.categorize_sentiment(0.04), 'neutral')
    
    def test_analyze_dataframe(self):
        """Test DataFrame sentiment analysis"""
        # Create sample data
        df = pd.DataFrame({
            'query': ['best python', 'worst errors', 'python tutorial'],
            'clicks': [100, 50, 75],
            'impressions': [1000, 500, 750],
            'ctr': [0.1, 0.1, 0.1],
            'position': [5.0, 10.0, 7.5]
        })
        
        result = self.analyzer.analyze_dataframe(df, min_impressions=0)
        
        # Check that sentiment columns were added
        self.assertIn('vader_compound', result.columns)
        self.assertIn('textblob_polarity', result.columns)
        
        # Check that we have the right number of rows
        self.assertEqual(len(result), 3)
    
    def test_identify_strengths_weaknesses(self):
        """Test strength and weakness identification"""
        # Create sample data with sentiment
        df = pd.DataFrame({
            'query': ['query1', 'query2', 'query3', 'query4', 'query5'],
            'clicks': [100, 50, 25, 10, 5],
            'impressions': [1000, 500, 250, 100, 50],
            'ctr': [0.1, 0.1, 0.1, 0.1, 0.1],
            'position': [1.0, 5.0, 10.0, 20.0, 30.0],
            'vader_compound': [0.8, 0.5, 0.0, -0.5, -0.8],
            'vader_positive': [0.8, 0.5, 0.0, 0.0, 0.0],
            'vader_negative': [0.0, 0.0, 0.0, 0.5, 0.8],
            'vader_neutral': [0.2, 0.5, 1.0, 0.5, 0.2],
            'textblob_polarity': [0.5, 0.3, 0.0, -0.3, -0.5],
            'textblob_subjectivity': [0.5, 0.5, 0.5, 0.5, 0.5]
        })
        
        results = self.analyzer.identify_strengths_weaknesses(df)
        
        self.assertIn('strengths', results)
        self.assertIn('weaknesses', results)
        self.assertIn('all_data', results)
        
        # Check that performance_score was added
        self.assertIn('performance_score', results['all_data'].columns)
        self.assertIn('sentiment_category', results['all_data'].columns)
    
    def test_extract_entities(self):
        """Test entity extraction"""
        # Only test if spaCy model is available
        if self.analyzer.nlp is None:
            self.skipTest("spaCy model not available")
        
        text = "Python tutorial by Google for beginners in New York"
        entities = self.analyzer.extract_entities(text)
        
        # Should be a list of tuples
        self.assertIsInstance(entities, list)
        
        if len(entities) > 0:
            self.assertIsInstance(entities[0], tuple)
            self.assertEqual(len(entities[0]), 2)
    
    def test_generate_insights(self):
        """Test insights generation"""
        # Create minimal analysis results
        df = pd.DataFrame({
            'query': ['query1', 'query2'],
            'clicks': [100, 50],
            'impressions': [1000, 500],
            'ctr': [0.1, 0.1],
            'position': [5.0, 10.0],
            'vader_compound': [0.5, -0.5],
            'vader_positive': [0.5, 0.0],
            'vader_negative': [0.0, 0.5],
            'vader_neutral': [0.5, 0.5],
            'textblob_polarity': [0.5, -0.5],
            'textblob_subjectivity': [0.5, 0.5],
            'sentiment_category': ['positive', 'negative'],
            'performance_score': [80.0, 20.0]
        })
        
        results = {
            'all_data': df,
            'strengths': df[df['sentiment_category'] == 'positive'],
            'weaknesses': df[df['sentiment_category'] == 'negative']
        }
        
        insights = self.analyzer.generate_insights(results)
        
        # Check that it's a string
        self.assertIsInstance(insights, str)
        
        # Check that it contains expected sections
        self.assertIn('OVERALL STATISTICS', insights)
        self.assertIn('SENTIMENT DISTRIBUTION', insights)
        self.assertIn('TOP STRENGTHS', insights)
        self.assertIn('TOP WEAKNESSES', insights)


class TestSentimentScores(unittest.TestCase):
    """Test sentiment scoring edge cases"""
    
    def setUp(self):
        """Set up test fixtures"""
        with patch('gsc_sentiment_analyzer.service_account.Credentials.from_service_account_file'):
            with patch('gsc_sentiment_analyzer.build'):
                self.analyzer = GSCSentimentAnalyzer(
                    credentials_path='fake_credentials.json',
                    site_url='https://example.com'
                )
    
    def test_empty_query(self):
        """Test sentiment analysis for empty query"""
        result = self.analyzer.analyze_query_sentiment("")
        self.assertIsInstance(result, dict)
        self.assertIn('vader_compound', result)
    
    def test_special_characters(self):
        """Test sentiment analysis with special characters"""
        query = "python!!! best??? tutorial###"
        result = self.analyzer.analyze_query_sentiment(query)
        self.assertIsInstance(result, dict)
    
    def test_numeric_query(self):
        """Test sentiment analysis with numbers"""
        query = "python 3.11 tutorial 2024"
        result = self.analyzer.analyze_query_sentiment(query)
        self.assertIsInstance(result, dict)


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestGSCSentimentAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestSentimentScores))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
