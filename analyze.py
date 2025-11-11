"""
Main Analysis Script for GSC Sentiment Analysis

This script ties together all components to perform comprehensive
sentiment analysis on Google Search Console data.
"""

import os
import sys
import json
import argparse
from datetime import datetime
import pandas as pd

from gsc_connector import GSCConnector
from sentiment_analyzer import SentimentAnalyzer
from entity_analyzer import EntityAnalyzer
from insights_generator import InsightsGenerator
from visualizations import create_visualizations


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Analyze sentiment and entities in Google Search Console data'
    )
    parser.add_argument(
        '--site',
        type=str,
        help='Site URL to analyze (if not provided, will list available sites)'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Number of days of data to analyze (default: 30)'
    )
    parser.add_argument(
        '--credentials',
        type=str,
        default='credentials.json',
        help='Path to Google OAuth credentials file'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='output',
        help='Output directory for reports and visualizations'
    )
    parser.add_argument(
        '--no-viz',
        action='store_true',
        help='Skip visualization generation'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    print("=" * 80)
    print("Google Search Console Sentiment Analysis")
    print("=" * 80)
    print()
    
    # Initialize GSC Connector
    print("Connecting to Google Search Console...")
    try:
        gsc = GSCConnector(credentials_path=args.credentials)
        gsc.authenticate()
        print("✓ Connected successfully")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        print("\nPlease follow these steps:")
        print("1. Go to Google Cloud Console (console.cloud.google.com)")
        print("2. Create a project and enable the Search Console API")
        print("3. Create OAuth 2.0 credentials")
        print("4. Download the credentials JSON file")
        print("5. Save it as 'credentials.json' in this directory")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error connecting: {e}")
        sys.exit(1)
    
    print()
    
    # Get site to analyze
    if not args.site:
        print("Available sites:")
        sites = gsc.list_sites()
        for i, site in enumerate(sites, 1):
            print(f"  {i}. {site}")
        print("\nPlease run again with --site parameter")
        sys.exit(0)
    
    site_url = args.site
    print(f"Analyzing site: {site_url}")
    print(f"Time period: Last {args.days} days")
    print()
    
    # Fetch data from GSC
    print("Fetching search analytics data...")
    try:
        gsc_data = gsc.get_recent_data(
            site_url=site_url,
            days=args.days,
            dimensions=['query', 'page']
        )
        
        if 'rows' not in gsc_data or len(gsc_data['rows']) == 0:
            print("✗ No data found for this site and time period")
            sys.exit(1)
        
        print(f"✓ Retrieved {len(gsc_data['rows'])} queries")
    except Exception as e:
        print(f"✗ Error fetching data: {e}")
        sys.exit(1)
    
    print()
    
    # Perform sentiment analysis
    print("Analyzing sentiment...")
    sentiment_analyzer = SentimentAnalyzer()
    df = sentiment_analyzer.analyze_dataset(gsc_data)
    sentiment_summary = sentiment_analyzer.get_sentiment_summary(df)
    print(f"✓ Analyzed {len(df)} queries")
    print()
    
    # Perform entity analysis
    print("Extracting entities...")
    entity_analyzer = EntityAnalyzer()
    df = entity_analyzer.analyze_query_entities(df)
    entity_analysis = entity_analyzer.identify_citation_opportunities(df)
    print(f"✓ Found {entity_analysis['total_entities']} unique entities")
    print(f"✓ Identified {entity_analysis['citation_ready_entities']} citation opportunities")
    print()
    
    # Generate insights
    print("Generating insights...")
    insights_gen = InsightsGenerator()
    insights = insights_gen.analyze_strengths_weaknesses(df, sentiment_summary)
    ai_strategy = insights_gen.generate_ai_citation_strategy(entity_analysis, df)
    print(f"✓ Found {len(insights['strengths'])} strengths")
    print(f"✓ Found {len(insights['weaknesses'])} weaknesses")
    print(f"✓ Identified {len(insights['opportunities'])} opportunities")
    print()
    
    # Save detailed data
    print("Saving results...")
    
    # Save DataFrame
    csv_path = os.path.join(args.output, 'detailed_analysis.csv')
    df.to_csv(csv_path, index=False)
    print(f"✓ Saved detailed analysis to {csv_path}")
    
    # Save summaries as JSON
    summary_data = {
        'site_url': site_url,
        'analysis_date': datetime.now().isoformat(),
        'time_period_days': args.days,
        'sentiment_summary': sentiment_summary,
        'entity_analysis': entity_analysis,
        'insights': insights,
        'ai_citation_strategy': ai_strategy
    }
    
    json_path = os.path.join(args.output, 'analysis_summary.json')
    with open(json_path, 'w') as f:
        json.dump(summary_data, f, indent=2, default=str)
    print(f"✓ Saved summary to {json_path}")
    
    # Generate text report
    report = insights_gen.generate_summary_report(
        df, sentiment_summary, entity_analysis, insights
    )
    
    report_path = os.path.join(args.output, 'analysis_report.txt')
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"✓ Saved report to {report_path}")
    
    # Print report to console
    print()
    print(report)
    
    # Generate visualizations
    if not args.no_viz:
        print()
        print("Generating visualizations...")
        try:
            viz_paths = create_visualizations(
                df, sentiment_summary, entity_analysis, args.output
            )
            for path in viz_paths:
                print(f"✓ Saved visualization to {path}")
        except Exception as e:
            print(f"✗ Error generating visualizations: {e}")
    
    print()
    print("=" * 80)
    print("Analysis complete!")
    print(f"Results saved to: {args.output}/")
    print("=" * 80)


if __name__ == '__main__':
    main()
