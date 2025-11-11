"""
Visualization module for GSC Sentiment Analysis

Provides various charts and visualizations for sentiment analysis results.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, Optional
import os


class SentimentVisualizer:
    """Creates visualizations for sentiment analysis results."""
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize the visualizer.
        
        Args:
            style: Matplotlib style to use
        """
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')
        
        sns.set_palette("husl")
        self.colors = {
            'positive': '#2ecc71',
            'neutral': '#95a5a6',
            'negative': '#e74c3c'
        }
    
    def plot_sentiment_distribution(
        self,
        df: pd.DataFrame,
        output_path: Optional[str] = None
    ):
        """
        Plot sentiment distribution pie chart.
        
        Args:
            df: DataFrame with sentiment_category column
            output_path: Path to save the plot (optional)
        """
        sentiment_counts = df['sentiment_category'].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = [self.colors[cat] for cat in sentiment_counts.index]
        
        ax.pie(
            sentiment_counts.values,
            labels=sentiment_counts.index,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        ax.set_title('Sentiment Distribution of Search Queries', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Saved sentiment distribution plot to {output_path}")
        
        plt.close()
    
    def plot_sentiment_vs_performance(
        self,
        df: pd.DataFrame,
        output_path: Optional[str] = None
    ):
        """
        Plot sentiment score vs performance metrics.
        
        Args:
            df: DataFrame with sentiment and performance data
            output_path: Path to save the plot (optional)
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Sentiment vs Clicks
        axes[0, 0].scatter(
            df['vader_compound'],
            df['clicks'],
            alpha=0.5,
            c=df['vader_compound'],
            cmap='RdYlGn'
        )
        axes[0, 0].set_xlabel('Sentiment Score')
        axes[0, 0].set_ylabel('Clicks')
        axes[0, 0].set_title('Sentiment vs Clicks')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Sentiment vs CTR
        axes[0, 1].scatter(
            df['vader_compound'],
            df['ctr'],
            alpha=0.5,
            c=df['vader_compound'],
            cmap='RdYlGn'
        )
        axes[0, 1].set_xlabel('Sentiment Score')
        axes[0, 1].set_ylabel('CTR')
        axes[0, 1].set_title('Sentiment vs CTR')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Sentiment vs Position
        axes[1, 0].scatter(
            df['vader_compound'],
            df['position'],
            alpha=0.5,
            c=df['vader_compound'],
            cmap='RdYlGn'
        )
        axes[1, 0].set_xlabel('Sentiment Score')
        axes[1, 0].set_ylabel('Position')
        axes[1, 0].set_title('Sentiment vs Position')
        axes[1, 0].invert_yaxis()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Sentiment distribution histogram
        axes[1, 1].hist(df['vader_compound'], bins=30, edgecolor='black', alpha=0.7)
        axes[1, 1].set_xlabel('Sentiment Score')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].set_title('Sentiment Score Distribution')
        axes[1, 1].axvline(0, color='red', linestyle='--', label='Neutral')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle('Sentiment Analysis Correlations', fontsize=16, fontweight='bold', y=1.00)
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Saved sentiment vs performance plot to {output_path}")
        
        plt.close()
    
    def plot_top_performers(
        self,
        strengths_df: pd.DataFrame,
        weaknesses_df: pd.DataFrame,
        top_n: int = 10,
        output_path: Optional[str] = None
    ):
        """
        Plot top strengths and weaknesses.
        
        Args:
            strengths_df: DataFrame with strengths
            weaknesses_df: DataFrame with weaknesses
            top_n: Number of top items to show
            output_path: Path to save the plot (optional)
        """
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        
        # Top strengths
        if len(strengths_df) > 0:
            top_strengths = strengths_df.head(top_n).copy()
            top_strengths['short_query'] = top_strengths['query'].apply(
                lambda x: x[:40] + '...' if len(x) > 40 else x
            )
            
            axes[0].barh(
                range(len(top_strengths)),
                top_strengths['performance_score'],
                color=self.colors['positive']
            )
            axes[0].set_yticks(range(len(top_strengths)))
            axes[0].set_yticklabels(top_strengths['short_query'])
            axes[0].set_xlabel('Performance Score')
            axes[0].set_title(f'Top {top_n} Strengths', fontweight='bold')
            axes[0].invert_yaxis()
            axes[0].grid(True, alpha=0.3, axis='x')
        
        # Top weaknesses
        if len(weaknesses_df) > 0:
            top_weaknesses = weaknesses_df.head(top_n).copy()
            top_weaknesses['short_query'] = top_weaknesses['query'].apply(
                lambda x: x[:40] + '...' if len(x) > 40 else x
            )
            
            axes[1].barh(
                range(len(top_weaknesses)),
                top_weaknesses['performance_score'],
                color=self.colors['negative']
            )
            axes[1].set_yticks(range(len(top_weaknesses)))
            axes[1].set_yticklabels(top_weaknesses['short_query'])
            axes[1].set_xlabel('Performance Score')
            axes[1].set_title(f'Top {top_n} Weaknesses', fontweight='bold')
            axes[1].invert_yaxis()
            axes[1].grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Saved top performers plot to {output_path}")
        
        plt.close()
    
    def plot_entity_analysis(
        self,
        entity_analysis: Dict,
        top_n: int = 15,
        output_path: Optional[str] = None
    ):
        """
        Plot entity analysis results.
        
        Args:
            entity_analysis: Dictionary with entity analysis results
            top_n: Number of top entities to show
            output_path: Path to save the plot (optional)
        """
        if not entity_analysis['top_entities']:
            print("No entities to visualize.")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        
        # Top entities by frequency
        top_entities = entity_analysis['top_entities'][:top_n]
        entities = [e['entity'] for e in top_entities]
        frequencies = [e['frequency'] for e in top_entities]
        
        axes[0].barh(range(len(entities)), frequencies, color='#3498db')
        axes[0].set_yticks(range(len(entities)))
        axes[0].set_yticklabels(entities)
        axes[0].set_xlabel('Frequency')
        axes[0].set_title(f'Top {top_n} Entities for AI Citations', fontweight='bold')
        axes[0].invert_yaxis()
        axes[0].grid(True, alpha=0.3, axis='x')
        
        # Entity types distribution
        if entity_analysis['entity_types']:
            entity_types = list(entity_analysis['entity_types'].keys())
            type_counts = list(entity_analysis['entity_types'].values())
            
            axes[1].pie(
                type_counts,
                labels=entity_types,
                autopct='%1.1f%%',
                startangle=90
            )
            axes[1].set_title('Entity Types Distribution', fontweight='bold')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Saved entity analysis plot to {output_path}")
        
        plt.close()
    
    def create_interactive_dashboard(
        self,
        df: pd.DataFrame,
        output_path: str = 'outputs/interactive_dashboard.html'
    ):
        """
        Create an interactive Plotly dashboard.
        
        Args:
            df: DataFrame with analysis results
            output_path: Path to save the HTML dashboard
        """
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Sentiment Distribution',
                'Performance Score vs Sentiment',
                'Top Queries by Clicks',
                'CTR vs Position'
            ),
            specs=[
                [{'type': 'pie'}, {'type': 'scatter'}],
                [{'type': 'bar'}, {'type': 'scatter'}]
            ]
        )
        
        # Sentiment distribution pie chart
        sentiment_counts = df['sentiment_category'].value_counts()
        fig.add_trace(
            go.Pie(
                labels=sentiment_counts.index,
                values=sentiment_counts.values,
                marker=dict(colors=[
                    self.colors[cat] for cat in sentiment_counts.index
                ])
            ),
            row=1, col=1
        )
        
        # Performance vs sentiment scatter
        fig.add_trace(
            go.Scatter(
                x=df['vader_compound'],
                y=df['performance_score'],
                mode='markers',
                marker=dict(
                    size=df['clicks'] / df['clicks'].max() * 20 + 5,
                    color=df['vader_compound'],
                    colorscale='RdYlGn',
                    showscale=True,
                    colorbar=dict(x=0.46, len=0.4)
                ),
                text=df['query'],
                hovertemplate='<b>%{text}</b><br>Sentiment: %{x:.2f}<br>Performance: %{y:.1f}<extra></extra>'
            ),
            row=1, col=2
        )
        
        # Top queries by clicks
        top_clicks = df.nlargest(15, 'clicks')
        fig.add_trace(
            go.Bar(
                x=top_clicks['clicks'],
                y=top_clicks['query'].apply(lambda x: x[:40] + '...' if len(x) > 40 else x),
                orientation='h',
                marker=dict(color='#3498db'),
                hovertemplate='<b>%{y}</b><br>Clicks: %{x}<extra></extra>'
            ),
            row=2, col=1
        )
        
        # CTR vs Position scatter
        fig.add_trace(
            go.Scatter(
                x=df['position'],
                y=df['ctr'],
                mode='markers',
                marker=dict(
                    size=df['impressions'] / df['impressions'].max() * 20 + 5,
                    color=df['vader_compound'],
                    colorscale='RdYlGn',
                    showscale=False
                ),
                text=df['query'],
                hovertemplate='<b>%{text}</b><br>Position: %{x:.1f}<br>CTR: %{y:.2%}<extra></extra>'
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="GSC Sentiment Analysis Dashboard",
            showlegend=False,
            height=800
        )
        
        fig.update_xaxes(title_text="Sentiment Score", row=1, col=2)
        fig.update_yaxes(title_text="Performance Score", row=1, col=2)
        
        fig.update_xaxes(title_text="Clicks", row=2, col=1)
        fig.update_yaxes(title_text="Query", row=2, col=1)
        
        fig.update_xaxes(title_text="Position", row=2, col=2)
        fig.update_yaxes(title_text="CTR", row=2, col=2)
        
        # Save
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        fig.write_html(output_path)
        print(f"Saved interactive dashboard to {output_path}")
    
    def generate_all_visualizations(
        self,
        analysis_results: Dict,
        output_dir: str = 'outputs'
    ):
        """
        Generate all visualizations.
        
        Args:
            analysis_results: Dictionary with all analysis results
            output_dir: Directory to save visualizations
        """
        os.makedirs(output_dir, exist_ok=True)
        
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        print("\nGenerating visualizations...")
        
        # Sentiment distribution
        self.plot_sentiment_distribution(
            analysis_results['all_data'],
            f"{output_dir}/sentiment_distribution_{timestamp}.png"
        )
        
        # Sentiment vs performance
        self.plot_sentiment_vs_performance(
            analysis_results['all_data'],
            f"{output_dir}/sentiment_vs_performance_{timestamp}.png"
        )
        
        # Top performers
        self.plot_top_performers(
            analysis_results['strengths'],
            analysis_results['weaknesses'],
            output_path=f"{output_dir}/top_performers_{timestamp}.png"
        )
        
        # Entity analysis
        if 'entity_analysis' in analysis_results:
            self.plot_entity_analysis(
                analysis_results['entity_analysis'],
                output_path=f"{output_dir}/entity_analysis_{timestamp}.png"
            )
        
        # Interactive dashboard
        self.create_interactive_dashboard(
            analysis_results['all_data'],
            output_path=f"{output_dir}/interactive_dashboard_{timestamp}.html"
        )
        
        print(f"\nAll visualizations saved to {output_dir}/")
