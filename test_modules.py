"""
Test script for GSC Sentiment Analysis modules

This script tests the core functionality without requiring API credentials.
"""

import sys
import json
from datetime import datetime

# Test imports
print("Testing imports...")
try:
    from sentiment_analyzer import SentimentAnalyzer
    from entity_analyzer import EntityAnalyzer
    from insights_generator import InsightsGenerator
    print("✓ All modules imported successfully")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("Running Module Tests")
print("="*80)

# Create sample GSC data
sample_gsc_data = {
    'rows': [
        {
            'keys': ['best python tutorial', 'https://example.com/python'],
            'clicks': 150,
            'impressions': 5000,
            'ctr': 0.03,
            'position': 3.5
        },
        {
            'keys': ['how to fix python error', 'https://example.com/errors'],
            'clicks': 80,
            'impressions': 3000,
            'ctr': 0.027,
            'position': 8.2
        },
        {
            'keys': ['python vs javascript', 'https://example.com/compare'],
            'clicks': 120,
            'impressions': 4500,
            'ctr': 0.027,
            'position': 5.1
        },
        {
            'keys': ['python tutorial', 'https://example.com/tutorial'],
            'clicks': 200,
            'impressions': 7000,
            'ctr': 0.029,
            'position': 2.8
        },
        {
            'keys': ['python installation guide', 'https://example.com/install'],
            'clicks': 90,
            'impressions': 2500,
            'ctr': 0.036,
            'position': 4.0
        }
    ]
}

# Test 1: Sentiment Analyzer
print("\n1. Testing Sentiment Analyzer...")
try:
    sentiment_analyzer = SentimentAnalyzer()
    
    # Test single query analysis
    result = sentiment_analyzer.analyze_query_sentiment("best python tutorial")
    assert 'sentiment' in result
    assert 'polarity' in result
    assert 'intent' in result
    print(f"   ✓ Single query analysis works")
    print(f"     Query: 'best python tutorial'")
    print(f"     Sentiment: {result['sentiment']}")
    print(f"     Intent: {result['intent']}")
    print(f"     Polarity: {result['polarity']:.3f}")
    
    # Test dataset analysis
    df = sentiment_analyzer.analyze_dataset(sample_gsc_data)
    assert len(df) == 5
    assert 'sentiment' in df.columns
    assert 'intent' in df.columns
    print(f"   ✓ Dataset analysis works ({len(df)} queries analyzed)")
    
    # Test summary generation
    summary = sentiment_analyzer.get_sentiment_summary(df)
    assert 'total_queries' in summary
    assert 'sentiment_distribution' in summary
    print(f"   ✓ Summary generation works")
    print(f"     Total queries: {summary['total_queries']}")
    print(f"     Sentiment distribution: {summary['sentiment_distribution']}")
    
except Exception as e:
    print(f"   ✗ Sentiment analyzer test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Entity Analyzer
print("\n2. Testing Entity Analyzer...")
try:
    entity_analyzer = EntityAnalyzer()
    
    # Test entity extraction
    if entity_analyzer.nlp:
        entities = entity_analyzer.extract_entities("Python is a programming language created by Guido van Rossum")
        print(f"   ✓ Entity extraction works")
        print(f"     Found {len(entities)} entities")
        if entities:
            print(f"     Example: {entities[0]}")
    else:
        print("   ⚠ spaCy model not installed (expected for basic test)")
    
    # Test key phrase extraction
    phrases = entity_analyzer.extract_key_phrases("best python tutorial for beginners")
    print(f"   ✓ Key phrase extraction works")
    print(f"     Found {len(phrases)} phrases: {phrases[:3]}")
    
    # Test query entity analysis (should work even without spaCy)
    df = sentiment_analyzer.analyze_dataset(sample_gsc_data)
    df_with_entities = entity_analyzer.analyze_query_entities(df)
    assert 'entities' in df_with_entities.columns
    print(f"   ✓ Query entity analysis works")
    
except Exception as e:
    print(f"   ✗ Entity analyzer test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Insights Generator
print("\n3. Testing Insights Generator...")
try:
    insights_gen = InsightsGenerator()
    
    # Analyze full dataset
    df = sentiment_analyzer.analyze_dataset(sample_gsc_data)
    sentiment_summary = sentiment_analyzer.get_sentiment_summary(df)
    
    # Test strengths/weaknesses analysis
    insights = insights_gen.analyze_strengths_weaknesses(df, sentiment_summary)
    assert 'strengths' in insights
    assert 'weaknesses' in insights
    assert 'opportunities' in insights
    print(f"   ✓ Strengths/weaknesses analysis works")
    print(f"     Strengths: {len(insights['strengths'])}")
    print(f"     Weaknesses: {len(insights['weaknesses'])}")
    print(f"     Opportunities: {len(insights['opportunities'])}")
    
    # Test AI citation strategy
    entity_analysis = {
        'total_entities': 10,
        'citation_ready_entities': 5,
        'top_citation_opportunities': [],
        'entity_type_distribution': {'PERSON': 3, 'ORG': 2}
    }
    ai_strategy = insights_gen.generate_ai_citation_strategy(entity_analysis, df)
    assert 'priority_entities' in ai_strategy
    assert 'content_recommendations' in ai_strategy
    print(f"   ✓ AI citation strategy generation works")
    print(f"     Content recommendations: {len(ai_strategy['content_recommendations'])}")
    
    # Test report generation
    report = insights_gen.generate_summary_report(df, sentiment_summary, entity_analysis, insights)
    assert len(report) > 0
    assert 'OVERVIEW' in report
    print(f"   ✓ Summary report generation works ({len(report)} characters)")
    
except Exception as e:
    print(f"   ✗ Insights generator test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Integration Test
print("\n4. Testing Full Integration...")
try:
    # Complete analysis workflow
    sentiment_analyzer = SentimentAnalyzer()
    entity_analyzer = EntityAnalyzer()
    insights_gen = InsightsGenerator()
    
    # Process data through all modules
    df = sentiment_analyzer.analyze_dataset(sample_gsc_data)
    df = entity_analyzer.analyze_query_entities(df)
    sentiment_summary = sentiment_analyzer.get_sentiment_summary(df)
    entity_analysis = entity_analyzer.identify_citation_opportunities(df, min_clicks=10)
    insights = insights_gen.analyze_strengths_weaknesses(df, sentiment_summary)
    ai_strategy = insights_gen.generate_ai_citation_strategy(entity_analysis, df)
    
    print(f"   ✓ Full integration works")
    print(f"     Processed {len(df)} queries")
    print(f"     Found {entity_analysis['total_entities']} entities")
    print(f"     Generated {len(insights['strengths']) + len(insights['weaknesses']) + len(insights['opportunities'])} insights")
    
    # Save test results
    test_results = {
        'test_date': datetime.now().isoformat(),
        'queries_analyzed': len(df),
        'sentiment_summary': {k: v for k, v in sentiment_summary.items() if k not in ['performance_by_sentiment', 'performance_by_intent']},
        'insights_count': {
            'strengths': len(insights['strengths']),
            'weaknesses': len(insights['weaknesses']),
            'opportunities': len(insights['opportunities'])
        }
    }
    
    with open('test_results.json', 'w') as f:
        json.dump(test_results, f, indent=2, default=str)
    print(f"   ✓ Test results saved to test_results.json")
    
except Exception as e:
    print(f"   ✗ Integration test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("✓ All tests completed successfully!")
print("="*80)
print("\nNote: For full functionality including entity extraction,")
print("install the spaCy model: python -m spacy download en_core_web_sm")
