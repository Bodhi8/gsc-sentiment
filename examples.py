"""
Example script demonstrating various use cases of the GSC Sentiment Analyzer
"""

from gsc_sentiment_analyzer import GSCSentimentAnalyzer
from visualizations import SentimentVisualizer
import os
from dotenv import load_dotenv
import pandas as pd


def example_basic_analysis():
    """Example 1: Basic sentiment analysis"""
    print("=" * 80)
    print("EXAMPLE 1: Basic Sentiment Analysis")
    print("=" * 80)
    
    load_dotenv()
    
    analyzer = GSCSentimentAnalyzer(
        credentials_path=os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
        site_url=os.getenv('SITE_URL')
    )
    
    # Fetch last 90 days
    from datetime import datetime, timedelta
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    
    df = analyzer.fetch_search_analytics(
        start_date=start_date,
        end_date=end_date,
        dimensions=['query', 'page'],
        max_rows=5000
    )
    
    df_analyzed = analyzer.analyze_dataframe(df, min_impressions=5)
    results = analyzer.identify_strengths_weaknesses(df_analyzed)
    entity_analysis = analyzer.analyze_entities_for_citations(df_analyzed, top_n=50)
    results['entity_analysis'] = entity_analysis
    
    print(analyzer.generate_insights(results))
    analyzer.save_results(results, output_dir='outputs/example1')


def example_comparative_analysis():
    """Example 2: Compare two time periods"""
    print("=" * 80)
    print("EXAMPLE 2: Comparative Analysis (Two Time Periods)")
    print("=" * 80)
    
    load_dotenv()
    
    analyzer = GSCSentimentAnalyzer(
        credentials_path=os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
        site_url=os.getenv('SITE_URL')
    )
    
    from datetime import datetime, timedelta
    
    # Period 1: Last 30 days
    end_date_1 = datetime.now()
    start_date_1 = end_date_1 - timedelta(days=30)
    
    # Period 2: Previous 30 days
    end_date_2 = start_date_1 - timedelta(days=1)
    start_date_2 = end_date_2 - timedelta(days=30)
    
    print(f"\nPeriod 1: {start_date_1.strftime('%Y-%m-%d')} to {end_date_1.strftime('%Y-%m-%d')}")
    df1 = analyzer.fetch_search_analytics(
        start_date=start_date_1.strftime('%Y-%m-%d'),
        end_date=end_date_1.strftime('%Y-%m-%d'),
        dimensions=['query'],
        max_rows=5000
    )
    df1_analyzed = analyzer.analyze_dataframe(df1, min_impressions=5)
    
    print(f"\nPeriod 2: {start_date_2.strftime('%Y-%m-%d')} to {end_date_2.strftime('%Y-%m-%d')}")
    df2 = analyzer.fetch_search_analytics(
        start_date=start_date_2.strftime('%Y-%m-%d'),
        end_date=end_date_2.strftime('%Y-%m-%d'),
        dimensions=['query'],
        max_rows=5000
    )
    df2_analyzed = analyzer.analyze_dataframe(df2, min_impressions=5)
    
    # Compare sentiment trends
    print("\n" + "=" * 80)
    print("COMPARISON RESULTS")
    print("=" * 80)
    
    print(f"\nPeriod 1 Stats:")
    print(f"  Average sentiment: {df1_analyzed['vader_compound'].mean():.3f}")
    print(f"  Positive queries: {len(df1_analyzed[df1_analyzed['vader_compound'] >= 0.05])}")
    print(f"  Negative queries: {len(df1_analyzed[df1_analyzed['vader_compound'] <= -0.05])}")
    print(f"  Total clicks: {df1_analyzed['clicks'].sum():,.0f}")
    
    print(f"\nPeriod 2 Stats:")
    print(f"  Average sentiment: {df2_analyzed['vader_compound'].mean():.3f}")
    print(f"  Positive queries: {len(df2_analyzed[df2_analyzed['vader_compound'] >= 0.05])}")
    print(f"  Negative queries: {len(df2_analyzed[df2_analyzed['vader_compound'] <= -0.05])}")
    print(f"  Total clicks: {df2_analyzed['clicks'].sum():,.0f}")
    
    # Identify sentiment shifts
    sentiment_change = df1_analyzed['vader_compound'].mean() - df2_analyzed['vader_compound'].mean()
    print(f"\nSentiment Change: {sentiment_change:+.3f}")
    
    if sentiment_change > 0.05:
        print("✅ Sentiment has improved significantly!")
    elif sentiment_change < -0.05:
        print("⚠️ Sentiment has declined - review negative queries")
    else:
        print("➡️ Sentiment is relatively stable")


def example_country_analysis():
    """Example 3: Analyze by country"""
    print("=" * 80)
    print("EXAMPLE 3: Country-Specific Analysis")
    print("=" * 80)
    
    load_dotenv()
    
    analyzer = GSCSentimentAnalyzer(
        credentials_path=os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
        site_url=os.getenv('SITE_URL')
    )
    
    from datetime import datetime, timedelta
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    
    # Fetch with country dimension
    df = analyzer.fetch_search_analytics(
        start_date=start_date,
        end_date=end_date,
        dimensions=['query', 'country'],
        max_rows=10000
    )
    
    # Analyze top countries
    top_countries = df.groupby('country')['clicks'].sum().nlargest(5).index
    
    for country in top_countries:
        print(f"\n{'=' * 80}")
        print(f"Analysis for: {country}")
        print('=' * 80)
        
        country_df = df[df['country'] == country].copy()
        country_analyzed = analyzer.analyze_dataframe(country_df, min_impressions=3)
        
        print(f"Total queries: {len(country_analyzed)}")
        print(f"Total clicks: {country_analyzed['clicks'].sum():,.0f}")
        print(f"Average sentiment: {country_analyzed['vader_compound'].mean():.3f}")
        
        # Show top positive and negative queries
        positive = country_analyzed.nlargest(3, 'vader_compound')
        negative = country_analyzed.nsmallest(3, 'vader_compound')
        
        print(f"\nTop positive queries:")
        for _, row in positive.iterrows():
            print(f"  • {row['query']} (sentiment: {row['vader_compound']:.3f})")
        
        print(f"\nTop negative queries:")
        for _, row in negative.iterrows():
            print(f"  • {row['query']} (sentiment: {row['vader_compound']:.3f})")


def example_entity_focus():
    """Example 4: Deep dive into entity analysis"""
    print("=" * 80)
    print("EXAMPLE 4: Entity Analysis for AI Citations")
    print("=" * 80)
    
    load_dotenv()
    
    analyzer = GSCSentimentAnalyzer(
        credentials_path=os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
        site_url=os.getenv('SITE_URL')
    )
    
    from datetime import datetime, timedelta
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
    
    df = analyzer.fetch_search_analytics(
        start_date=start_date,
        end_date=end_date,
        dimensions=['query', 'page'],
        max_rows=10000
    )
    
    df_analyzed = analyzer.analyze_dataframe(df, min_impressions=5)
    
    # Analyze entities from top 100 queries
    entity_analysis = analyzer.analyze_entities_for_citations(df_analyzed, top_n=100)
    
    print(f"\nTotal unique entities found: {len(set([e['entity'] for e in entity_analysis['top_entities']]))}")
    print(f"\nEntity types detected:")
    for entity_type, count in entity_analysis['entity_types'].items():
        print(f"  - {entity_type}: {count}")
    
    print(f"\n{'=' * 80}")
    print("Top 20 Entities for AI Citation Optimization")
    print('=' * 80)
    
    for i, entity_info in enumerate(entity_analysis['top_entities'][:20], 1):
        print(f"\n{i}. {entity_info['entity']} ({entity_info['type']})")
        print(f"   Frequency: {entity_info['frequency']} occurrences")
        print(f"   Sample queries:")
        for query in entity_info['sample_queries'][:3]:
            print(f"     • {query}")
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS FOR AI CITATIONS")
    print("=" * 80)
    print("""
These entities represent your content's authority signals. To optimize for AI citations:

1. Create comprehensive content about top entities
2. Ensure factual accuracy and credibility
3. Use structured data (Schema.org) for these entities
4. Build internal linking around entity topics
5. Create entity-focused FAQ sections
6. Update content to reflect current information about these entities
""")


def example_with_visualizations():
    """Example 5: Full analysis with visualizations"""
    print("=" * 80)
    print("EXAMPLE 5: Complete Analysis with Visualizations")
    print("=" * 80)
    
    load_dotenv()
    
    analyzer = GSCSentimentAnalyzer(
        credentials_path=os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
        site_url=os.getenv('SITE_URL')
    )
    
    from datetime import datetime, timedelta
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    
    print(f"\nFetching data from {start_date} to {end_date}...")
    df = analyzer.fetch_search_analytics(
        start_date=start_date,
        end_date=end_date,
        dimensions=['query', 'page'],
        max_rows=10000
    )
    
    print("Analyzing sentiment...")
    df_analyzed = analyzer.analyze_dataframe(df, min_impressions=5)
    
    print("Identifying strengths and weaknesses...")
    results = analyzer.identify_strengths_weaknesses(df_analyzed)
    
    print("Analyzing entities...")
    entity_analysis = analyzer.analyze_entities_for_citations(df_analyzed, top_n=100)
    results['entity_analysis'] = entity_analysis
    
    print("Generating reports...")
    analyzer.save_results(results, output_dir='outputs/example5')
    
    print("Creating visualizations...")
    visualizer = SentimentVisualizer()
    visualizer.generate_all_visualizations(results, output_dir='outputs/example5')
    
    print("\n✅ Analysis complete! Check the outputs/example5/ directory for results.")


def main():
    """Run example demonstrations"""
    print("\nGSC Sentiment Analyzer - Example Usage\n")
    print("Select an example to run:")
    print("1. Basic Sentiment Analysis")
    print("2. Comparative Analysis (Two Time Periods)")
    print("3. Country-Specific Analysis")
    print("4. Entity Analysis for AI Citations")
    print("5. Complete Analysis with Visualizations")
    print("6. Run all examples")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    examples = {
        '1': example_basic_analysis,
        '2': example_comparative_analysis,
        '3': example_country_analysis,
        '4': example_entity_focus,
        '5': example_with_visualizations,
    }
    
    if choice == '6':
        for func in examples.values():
            try:
                func()
                print("\n" * 3)
            except Exception as e:
                print(f"Error running example: {e}")
    elif choice in examples:
        try:
            examples[choice]()
        except Exception as e:
            print(f"Error running example: {e}")
    else:
        print("Invalid choice!")


if __name__ == '__main__':
    main()
