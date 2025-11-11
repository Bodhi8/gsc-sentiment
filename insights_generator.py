"""
Insights Generator for Search Console Analysis

This module generates actionable insights about site strengths,
weaknesses, and optimization opportunities.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict


class InsightsGenerator:
    """Generate insights from sentiment and entity analysis."""
    
    def __init__(self):
        """Initialize insights generator."""
        pass
    
    def analyze_strengths_weaknesses(
        self,
        df: pd.DataFrame,
        sentiment_summary: Dict
    ) -> Dict:
        """
        Identify site strengths and weaknesses based on performance data.
        
        Args:
            df: DataFrame with analysis results
            sentiment_summary: Summary statistics from sentiment analysis
            
        Returns:
            Dictionary with strengths and weaknesses
        """
        strengths = []
        weaknesses = []
        opportunities = []
        
        if df.empty:
            return {
                'strengths': strengths,
                'weaknesses': weaknesses,
                'opportunities': opportunities
            }
        
        # Analyze sentiment performance
        if 'performance_by_sentiment' in sentiment_summary:
            perf = sentiment_summary['performance_by_sentiment']
            
            # Check positive query performance
            if 'positive' in perf:
                pos_data = perf['positive']
                if pos_data.get('position', 100) < 5:
                    strengths.append({
                        'category': 'Sentiment',
                        'type': 'Positive Query Ranking',
                        'description': f"Strong rankings (avg pos {pos_data['position']:.1f}) for positive sentiment queries",
                        'impact': 'high',
                        'clicks': int(pos_data.get('clicks', 0))
                    })
                elif pos_data.get('position', 100) > 15:
                    weaknesses.append({
                        'category': 'Sentiment',
                        'type': 'Positive Query Ranking',
                        'description': f"Weak rankings (avg pos {pos_data['position']:.1f}) for positive sentiment queries",
                        'impact': 'high',
                        'opportunity': 'Optimize content for positive/buying intent queries'
                    })
            
            # Check negative query handling
            if 'negative' in perf:
                neg_data = perf['negative']
                if neg_data.get('clicks', 0) > 1000:
                    if neg_data.get('position', 100) < 10:
                        strengths.append({
                            'category': 'Content',
                            'type': 'Problem-Solving Content',
                            'description': f"Strong presence for problem/troubleshooting queries ({neg_data['clicks']:.0f} clicks)",
                            'impact': 'medium',
                            'clicks': int(neg_data.get('clicks', 0))
                        })
                    else:
                        opportunities.append({
                            'category': 'Content Gap',
                            'type': 'Problem-Solving',
                            'description': 'High interest in problem-solving queries but rankings could improve',
                            'recommendation': 'Create comprehensive troubleshooting guides and FAQs',
                            'potential_clicks': int(neg_data.get('impressions', 0) * 0.05)
                        })
        
        # Analyze intent performance
        if 'performance_by_intent' in sentiment_summary:
            intent_perf = sentiment_summary['performance_by_intent']
            
            # Check informational content strength
            if 'informational' in intent_perf:
                info_data = intent_perf['informational']
                if info_data.get('clicks', 0) > df['clicks'].sum() * 0.5:
                    strengths.append({
                        'category': 'Intent',
                        'type': 'Informational Content',
                        'description': f"Majority of traffic ({info_data['clicks']:.0f} clicks) from informational queries",
                        'impact': 'high',
                        'clicks': int(info_data.get('clicks', 0))
                    })
            
            # Check commercial intent
            if 'commercial' in intent_perf:
                comm_data = intent_perf['commercial']
                comm_clicks = comm_data.get('clicks', 0)
                total_clicks = df['clicks'].sum()
                
                if total_clicks > 0 and comm_clicks / total_clicks < 0.1:
                    opportunities.append({
                        'category': 'Intent Gap',
                        'type': 'Commercial Intent',
                        'description': f'Low commercial intent traffic ({comm_clicks:.0f} clicks, {comm_clicks/total_clicks*100:.1f}%)',
                        'recommendation': 'Add product reviews, comparisons, and buying guides',
                        'potential_clicks': int(total_clicks * 0.15)
                    })
        
        # Analyze CTR performance
        avg_ctr = sentiment_summary.get('avg_ctr', 0)
        if avg_ctr < 0.02:
            weaknesses.append({
                'category': 'CTR',
                'type': 'Low Click-Through Rate',
                'description': f'Overall CTR is low at {avg_ctr*100:.2f}%',
                'impact': 'high',
                'opportunity': 'Optimize meta titles and descriptions for better CTR'
            })
        elif avg_ctr > 0.05:
            strengths.append({
                'category': 'CTR',
                'type': 'Strong Click-Through Rate',
                'description': f'Excellent CTR at {avg_ctr*100:.2f}%',
                'impact': 'high',
                'clicks': int(sentiment_summary.get('total_clicks', 0))
            })
        
        # Analyze position performance
        avg_position = sentiment_summary.get('avg_position', 100)
        if avg_position < 5:
            strengths.append({
                'category': 'Rankings',
                'type': 'Top Rankings',
                'description': f'Strong average position at {avg_position:.1f}',
                'impact': 'high',
                'clicks': int(sentiment_summary.get('total_clicks', 0))
            })
        elif avg_position > 20:
            weaknesses.append({
                'category': 'Rankings',
                'type': 'Low Average Position',
                'description': f'Weak average position at {avg_position:.1f}',
                'impact': 'high',
                'opportunity': 'Focus on improving content quality and on-page SEO'
            })
        
        # Check for long-tail opportunities
        long_tail_queries = df[df['query_length'] >= 5]
        if len(long_tail_queries) > 0:
            long_tail_clicks = long_tail_queries['clicks'].sum()
            total_clicks = df['clicks'].sum()
            
            if total_clicks > 0:
                long_tail_ratio = long_tail_clicks / total_clicks
                
                if long_tail_ratio > 0.4:
                    strengths.append({
                        'category': 'Query Types',
                        'type': 'Long-Tail Queries',
                        'description': f'Strong long-tail presence ({long_tail_ratio*100:.1f}% of clicks)',
                        'impact': 'medium',
                        'clicks': int(long_tail_clicks)
                    })
                elif long_tail_ratio < 0.15:
                    opportunities.append({
                        'category': 'Query Expansion',
                        'type': 'Long-Tail Opportunity',
                        'description': 'Potential to capture more long-tail traffic',
                        'recommendation': 'Create detailed, specific content targeting long-tail queries',
                        'potential_clicks': int(total_clicks * 0.25)
                    })
        
        return {
            'strengths': sorted(strengths, key=lambda x: x.get('clicks', 0), reverse=True),
            'weaknesses': weaknesses,
            'opportunities': sorted(opportunities, key=lambda x: x.get('potential_clicks', 0), reverse=True)
        }
    
    def generate_ai_citation_strategy(
        self,
        entity_analysis: Dict,
        df: pd.DataFrame
    ) -> Dict:
        """
        Generate strategy for improving AI citation potential.
        
        Args:
            entity_analysis: Entity analysis results
            df: DataFrame with analysis results
            
        Returns:
            Strategy recommendations
        """
        strategy = {
            'priority_entities': [],
            'content_recommendations': [],
            'structured_data_needs': [],
            'authority_building': []
        }
        
        # Priority entities from citation opportunities
        if 'top_citation_opportunities' in entity_analysis:
            top_opps = entity_analysis['top_citation_opportunities'][:5]
            
            for opp in top_opps:
                strategy['priority_entities'].append({
                    'entity': opp['entity'],
                    'type': opp['entity_type'],
                    'current_position': opp['avg_position'],
                    'traffic': opp['clicks'],
                    'action': opp['recommendation']
                })
        
        # Content recommendations based on entity types
        if 'entity_type_distribution' in entity_analysis:
            entity_types = entity_analysis['entity_type_distribution']
            
            if entity_types.get('PERSON', 0) > 5:
                strategy['content_recommendations'].append({
                    'type': 'Expert Profiles',
                    'priority': 'high',
                    'description': 'Create authoritative expert profiles and author pages',
                    'ai_impact': 'Helps AI understand expertise and authority'
                })
            
            if entity_types.get('PRODUCT', 0) > 5:
                strategy['content_recommendations'].append({
                    'type': 'Product Reviews',
                    'priority': 'high',
                    'description': 'Develop comprehensive product reviews with specs and comparisons',
                    'ai_impact': 'AI models prefer detailed, factual product information'
                })
            
            if entity_types.get('ORG', 0) > 5:
                strategy['content_recommendations'].append({
                    'type': 'Organization Profiles',
                    'priority': 'medium',
                    'description': 'Build detailed organization profiles with key facts',
                    'ai_impact': 'Establishes entity relationships for knowledge graphs'
                })
        
        # Structured data recommendations
        strategy['structured_data_needs'] = [
            {
                'schema_type': 'Article',
                'priority': 'high',
                'reason': 'Essential for AI understanding of content structure'
            },
            {
                'schema_type': 'FAQPage',
                'priority': 'high',
                'reason': 'Directly feeds AI answer generation'
            },
            {
                'schema_type': 'HowTo',
                'priority': 'medium',
                'reason': 'Helps AI extract step-by-step information'
            },
            {
                'schema_type': 'Person/Organization',
                'priority': 'medium',
                'reason': 'Builds authority and entity recognition'
            }
        ]
        
        # Authority building recommendations
        avg_position = df['position'].mean() if not df.empty else 50
        
        if avg_position > 10:
            strategy['authority_building'].append({
                'action': 'Improve E-E-A-T signals',
                'priority': 'high',
                'tactics': [
                    'Add author bios with credentials',
                    'Include publication dates and update timestamps',
                    'Link to authoritative sources',
                    'Add expert quotes and citations'
                ]
            })
        
        strategy['authority_building'].append({
            'action': 'Create linkable assets',
            'priority': 'high',
            'tactics': [
                'Develop original research and data',
                'Create comprehensive guides and resources',
                'Build interactive tools and calculators',
                'Publish case studies with results'
            ]
        })
        
        return strategy
    
    def generate_summary_report(
        self,
        df: pd.DataFrame,
        sentiment_summary: Dict,
        entity_analysis: Dict,
        insights: Dict
    ) -> str:
        """
        Generate a comprehensive text summary report.
        
        Args:
            df: Analyzed DataFrame
            sentiment_summary: Sentiment analysis summary
            entity_analysis: Entity analysis results
            insights: Strengths and weaknesses
            
        Returns:
            Formatted summary report as string
        """
        report = []
        report.append("=" * 80)
        report.append("GOOGLE SEARCH CONSOLE SENTIMENT ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Overview
        report.append("OVERVIEW")
        report.append("-" * 80)
        report.append(f"Total Queries Analyzed: {sentiment_summary.get('total_queries', 0):,}")
        report.append(f"Total Clicks: {sentiment_summary.get('total_clicks', 0):,}")
        report.append(f"Total Impressions: {sentiment_summary.get('total_impressions', 0):,}")
        report.append(f"Average CTR: {sentiment_summary.get('avg_ctr', 0)*100:.2f}%")
        report.append(f"Average Position: {sentiment_summary.get('avg_position', 0):.2f}")
        report.append("")
        
        # Sentiment Distribution
        if 'sentiment_distribution' in sentiment_summary:
            report.append("SENTIMENT DISTRIBUTION")
            report.append("-" * 80)
            for sentiment, count in sentiment_summary['sentiment_distribution'].items():
                pct = count / sentiment_summary['total_queries'] * 100
                report.append(f"  {sentiment.capitalize()}: {count:,} queries ({pct:.1f}%)")
            report.append("")
        
        # Intent Distribution
        if 'intent_distribution' in sentiment_summary:
            report.append("SEARCH INTENT DISTRIBUTION")
            report.append("-" * 80)
            for intent, count in sentiment_summary['intent_distribution'].items():
                pct = count / sentiment_summary['total_queries'] * 100
                report.append(f"  {intent.capitalize()}: {count:,} queries ({pct:.1f}%)")
            report.append("")
        
        # Strengths
        if insights.get('strengths'):
            report.append("STRENGTHS")
            report.append("-" * 80)
            for i, strength in enumerate(insights['strengths'][:5], 1):
                report.append(f"{i}. {strength['type']} ({strength['category']})")
                report.append(f"   {strength['description']}")
                report.append(f"   Impact: {strength['impact'].upper()}")
                report.append("")
        
        # Weaknesses
        if insights.get('weaknesses'):
            report.append("WEAKNESSES")
            report.append("-" * 80)
            for i, weakness in enumerate(insights['weaknesses'][:5], 1):
                report.append(f"{i}. {weakness['type']} ({weakness['category']})")
                report.append(f"   {weakness['description']}")
                report.append(f"   Impact: {weakness['impact'].upper()}")
                if 'opportunity' in weakness:
                    report.append(f"   Fix: {weakness['opportunity']}")
                report.append("")
        
        # Opportunities
        if insights.get('opportunities'):
            report.append("OPPORTUNITIES")
            report.append("-" * 80)
            for i, opp in enumerate(insights['opportunities'][:5], 1):
                report.append(f"{i}. {opp['type']} ({opp['category']})")
                report.append(f"   {opp['description']}")
                report.append(f"   Recommendation: {opp['recommendation']}")
                if 'potential_clicks' in opp:
                    report.append(f"   Potential: {opp['potential_clicks']:,} additional clicks")
                report.append("")
        
        # Entity Analysis
        if entity_analysis.get('top_citation_opportunities'):
            report.append("TOP AI CITATION OPPORTUNITIES")
            report.append("-" * 80)
            for i, entity in enumerate(entity_analysis['top_citation_opportunities'][:5], 1):
                report.append(f"{i}. {entity['entity']} ({entity['entity_type']})")
                report.append(f"   Traffic: {entity['clicks']:,} clicks, {entity['impressions']:,} impressions")
                report.append(f"   Position: {entity['avg_position']:.1f}")
                report.append(f"   Action: {entity['recommendation']}")
                report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)
