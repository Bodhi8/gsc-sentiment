"""
Visualization Module for GSC Sentiment Analysis

Create visual reports and charts for sentiment and entity analysis.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List
import numpy as np


def create_visualizations(
    df: pd.DataFrame,
    sentiment_summary: Dict,
    entity_analysis: Dict,
    output_dir: str
) -> List[str]:
    """
    Create all visualizations for the analysis.
    
    Args:
        df: Analyzed DataFrame
        sentiment_summary: Sentiment summary statistics
        entity_analysis: Entity analysis results
        output_dir: Directory to save visualizations
        
    Returns:
        List of paths to created visualizations
    """
    saved_files = []
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 6)
    
    # 1. Sentiment Distribution Pie Chart
    if 'sentiment_distribution' in sentiment_summary:
        fig, ax = plt.subplots(figsize=(10, 8))
        
        sentiment_data = sentiment_summary['sentiment_distribution']
        colors = {'positive': '#4CAF50', 'neutral': '#FFC107', 'negative': '#F44336'}
        color_list = [colors.get(s, '#999999') for s in sentiment_data.keys()]
        
        wedges, texts, autotexts = ax.pie(
            sentiment_data.values(),
            labels=sentiment_data.keys(),
            autopct='%1.1f%%',
            colors=color_list,
            startangle=90
        )
        
        for text in texts:
            text.set_fontsize(12)
            text.set_weight('bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
        
        ax.set_title('Query Sentiment Distribution', fontsize=16, weight='bold', pad=20)
        
        path = os.path.join(output_dir, 'sentiment_distribution.png')
        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        saved_files.append(path)
    
    # 2. Intent Distribution Bar Chart
    if 'intent_distribution' in sentiment_summary:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        intent_data = sentiment_summary['intent_distribution']
        intents = list(intent_data.keys())
        counts = list(intent_data.values())
        
        bars = ax.bar(intents, counts, color='#2196F3', alpha=0.8)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontsize=10, weight='bold'
            )
        
        ax.set_xlabel('Search Intent', fontsize=12, weight='bold')
        ax.set_ylabel('Number of Queries', fontsize=12, weight='bold')
        ax.set_title('Search Intent Distribution', fontsize=16, weight='bold', pad=20)
        ax.tick_params(axis='x', rotation=45)
        
        path = os.path.join(output_dir, 'intent_distribution.png')
        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        saved_files.append(path)
    
    # 3. Performance by Sentiment
    if 'performance_by_sentiment' in sentiment_summary and df is not None and not df.empty:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        perf_data = sentiment_summary['performance_by_sentiment']
        sentiments = list(perf_data.keys())
        
        # Clicks by sentiment
        clicks = [perf_data[s]['clicks'] for s in sentiments]
        axes[0, 0].bar(sentiments, clicks, color=['#4CAF50', '#999999', '#F44336'][:len(sentiments)])
        axes[0, 0].set_title('Clicks by Sentiment', fontsize=12, weight='bold')
        axes[0, 0].set_ylabel('Clicks', fontsize=10)
        
        # CTR by sentiment
        ctrs = [perf_data[s]['ctr'] * 100 for s in sentiments]
        axes[0, 1].bar(sentiments, ctrs, color=['#4CAF50', '#999999', '#F44336'][:len(sentiments)])
        axes[0, 1].set_title('CTR by Sentiment', fontsize=12, weight='bold')
        axes[0, 1].set_ylabel('CTR (%)', fontsize=10)
        
        # Position by sentiment
        positions = [perf_data[s]['position'] for s in sentiments]
        axes[1, 0].bar(sentiments, positions, color=['#4CAF50', '#999999', '#F44336'][:len(sentiments)])
        axes[1, 0].set_title('Average Position by Sentiment', fontsize=12, weight='bold')
        axes[1, 0].set_ylabel('Position', fontsize=10)
        axes[1, 0].invert_yaxis()  # Lower position is better
        
        # Impressions by sentiment
        impressions = [perf_data[s]['impressions'] for s in sentiments]
        axes[1, 1].bar(sentiments, impressions, color=['#4CAF50', '#999999', '#F44336'][:len(sentiments)])
        axes[1, 1].set_title('Impressions by Sentiment', fontsize=12, weight='bold')
        axes[1, 1].set_ylabel('Impressions', fontsize=10)
        
        plt.suptitle('Performance Metrics by Sentiment', fontsize=16, weight='bold', y=1.00)
        
        path = os.path.join(output_dir, 'performance_by_sentiment.png')
        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        saved_files.append(path)
    
    # 4. Top Entities Chart
    if 'top_citation_opportunities' in entity_analysis and entity_analysis['top_citation_opportunities']:
        fig, ax = plt.subplots(figsize=(12, 8))
        
        top_entities = entity_analysis['top_citation_opportunities'][:10]
        entities = [e['entity'] for e in top_entities]
        clicks = [e['clicks'] for e in top_entities]
        
        y_pos = np.arange(len(entities))
        bars = ax.barh(y_pos, clicks, color='#9C27B0', alpha=0.8)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(entities, fontsize=10)
        ax.invert_yaxis()
        ax.set_xlabel('Clicks', fontsize=12, weight='bold')
        ax.set_title('Top 10 Entities by Traffic', fontsize=16, weight='bold', pad=20)
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(
                width, bar.get_y() + bar.get_height()/2.,
                f'{int(width):,}',
                ha='left', va='center', fontsize=9, weight='bold'
            )
        
        path = os.path.join(output_dir, 'top_entities.png')
        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        saved_files.append(path)
    
    # 5. CTR vs Position Scatter Plot
    if df is not None and not df.empty and 'ctr' in df.columns and 'position' in df.columns:
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Sample data if too many points
        plot_df = df.sample(min(500, len(df)))
        
        # Create scatter plot with color by sentiment
        sentiment_colors = {'positive': '#4CAF50', 'neutral': '#FFC107', 'negative': '#F44336'}
        
        for sentiment in plot_df['sentiment'].unique():
            sentiment_data = plot_df[plot_df['sentiment'] == sentiment]
            ax.scatter(
                sentiment_data['position'],
                sentiment_data['ctr'] * 100,
                alpha=0.6,
                s=sentiment_data['clicks'] * 2 + 10,
                c=sentiment_colors.get(sentiment, '#999999'),
                label=sentiment.capitalize()
            )
        
        ax.set_xlabel('Position', fontsize=12, weight='bold')
        ax.set_ylabel('CTR (%)', fontsize=12, weight='bold')
        ax.set_title('CTR vs Position by Sentiment', fontsize=16, weight='bold', pad=20)
        ax.legend(loc='upper right', fontsize=10)
        ax.invert_xaxis()  # Lower position numbers are better
        ax.grid(True, alpha=0.3)
        
        path = os.path.join(output_dir, 'ctr_vs_position.png')
        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        saved_files.append(path)
    
    # 6. Query Length Distribution
    if df is not None and not df.empty and 'query_length' in df.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        query_lengths = df['query_length'].value_counts().sort_index()
        
        ax.bar(query_lengths.index, query_lengths.values, color='#00BCD4', alpha=0.8)
        ax.set_xlabel('Query Length (words)', fontsize=12, weight='bold')
        ax.set_ylabel('Number of Queries', fontsize=12, weight='bold')
        ax.set_title('Query Length Distribution', fontsize=16, weight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='y')
        
        path = os.path.join(output_dir, 'query_length_distribution.png')
        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        saved_files.append(path)
    
    return saved_files
