"""
Entity Extraction and AI Citation Analysis

This module extracts entities from search queries and content,
analyzing which entities drive traffic and could help with AI citations.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Set, Tuple
import re
from collections import Counter, defaultdict
import spacy
from textblob import TextBlob


class EntityAnalyzer:
    """Analyze entities in search queries and identify AI citation opportunities."""
    
    def __init__(self, model_name: str = 'en_core_web_sm'):
        """
        Initialize entity analyzer.
        
        Args:
            model_name: spaCy model to use for NER
        """
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            print(f"Model {model_name} not found. Install it with: python -m spacy download {model_name}")
            self.nlp = None
        
        # Common entity types that matter for AI citations
        self.citation_entity_types = {
            'PERSON', 'ORG', 'PRODUCT', 'WORK_OF_ART', 'LAW',
            'GPE', 'EVENT', 'FAC', 'NORP'
        }
    
    def extract_entities(self, text: str) -> List[Dict]:
        """
        Extract named entities from text.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of entities with their types and metadata
        """
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            })
        
        return entities
    
    def extract_key_phrases(self, text: str) -> List[str]:
        """
        Extract key phrases using noun chunks.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of key phrases
        """
        if not self.nlp:
            # Fallback to simple n-gram extraction
            words = text.lower().split()
            phrases = []
            for i in range(len(words) - 1):
                phrases.append(' '.join(words[i:i+2]))
            return list(set(phrases))[:10]
        
        doc = self.nlp(text)
        phrases = [chunk.text.lower() for chunk in doc.noun_chunks]
        return list(set(phrases))
    
    def analyze_query_entities(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract entities from all queries in the dataset.
        
        Args:
            df: DataFrame with search queries
            
        Returns:
            DataFrame with entity information added
        """
        if 'query' not in df.columns:
            return df
        
        entities_list = []
        key_phrases_list = []
        
        for query in df['query']:
            entities = self.extract_entities(query)
            key_phrases = self.extract_key_phrases(query)
            
            entities_list.append(entities)
            key_phrases_list.append(key_phrases)
        
        df['entities'] = entities_list
        df['key_phrases'] = key_phrases_list
        df['entity_count'] = df['entities'].apply(len)
        
        return df
    
    def get_top_entities(
        self,
        df: pd.DataFrame,
        min_impressions: int = 100
    ) -> pd.DataFrame:
        """
        Get top performing entities across all queries.
        
        Args:
            df: DataFrame with entity analysis
            min_impressions: Minimum impressions to consider
            
        Returns:
            DataFrame with top entities and their performance
        """
        if 'entities' not in df.columns:
            df = self.analyze_query_entities(df)
        
        # Flatten entities with their metrics
        entity_data = []
        
        for _, row in df.iterrows():
            if row['impressions'] < min_impressions:
                continue
            
            for entity in row['entities']:
                entity_data.append({
                    'entity': entity['text'],
                    'entity_type': entity['label'],
                    'clicks': row['clicks'],
                    'impressions': row['impressions'],
                    'ctr': row['ctr'],
                    'position': row['position']
                })
        
        if not entity_data:
            return pd.DataFrame()
        
        entity_df = pd.DataFrame(entity_data)
        
        # Aggregate by entity
        entity_summary = entity_df.groupby(['entity', 'entity_type']).agg({
            'clicks': 'sum',
            'impressions': 'sum',
            'ctr': 'mean',
            'position': 'mean'
        }).reset_index()
        
        entity_summary['queries_count'] = entity_df.groupby(['entity', 'entity_type']).size().values
        entity_summary = entity_summary.sort_values('clicks', ascending=False)
        
        return entity_summary
    
    def identify_citation_opportunities(
        self,
        df: pd.DataFrame,
        min_clicks: int = 50
    ) -> Dict:
        """
        Identify entities and topics that present AI citation opportunities.
        
        Args:
            df: DataFrame with entity analysis
            min_clicks: Minimum clicks to consider
            
        Returns:
            Dictionary with citation opportunities and recommendations
        """
        if 'entities' not in df.columns:
            df = self.analyze_query_entities(df)
        
        top_entities = self.get_top_entities(df, min_impressions=min_clicks * 2)
        
        if top_entities.empty:
            return {
                'total_entities': 0,
                'citation_ready_entities': [],
                'recommendations': []
            }
        
        # Filter for citation-worthy entity types
        citation_entities = top_entities[
            top_entities['entity_type'].isin(self.citation_entity_types)
        ]
        
        # Identify high-performing entities
        high_performers = citation_entities[
            (citation_entities['clicks'] >= min_clicks) &
            (citation_entities['position'] <= 10)
        ].head(20)
        
        recommendations = []
        
        for _, entity in high_performers.iterrows():
            rec = {
                'entity': entity['entity'],
                'entity_type': entity['entity_type'],
                'clicks': int(entity['clicks']),
                'impressions': int(entity['impressions']),
                'avg_position': round(entity['position'], 2),
                'avg_ctr': round(entity['ctr'], 4),
                'recommendation': self._generate_recommendation(entity)
            }
            recommendations.append(rec)
        
        return {
            'total_entities': len(top_entities),
            'citation_ready_entities': len(citation_entities),
            'top_citation_opportunities': recommendations,
            'entity_type_distribution': citation_entities['entity_type'].value_counts().to_dict()
        }
    
    def _generate_recommendation(self, entity_row: pd.Series) -> str:
        """Generate a recommendation for an entity."""
        entity_type = entity_row['entity_type']
        position = entity_row['position']
        ctr = entity_row['ctr']
        
        if position <= 3:
            strength = "Strong"
        elif position <= 10:
            strength = "Moderate"
        else:
            strength = "Weak"
        
        rec = f"{strength} AI citation opportunity. "
        
        if entity_type == 'PERSON':
            rec += "Build authoritative content about this person with structured data."
        elif entity_type == 'ORG':
            rec += "Create comprehensive org profile with key facts and relationships."
        elif entity_type == 'PRODUCT':
            rec += "Develop detailed product reviews and comparisons with specs."
        elif entity_type in ['GPE', 'LOC']:
            rec += "Add location-specific insights with geographic context."
        else:
            rec += "Enhance content with factual, citable information."
        
        if ctr < 0.02:
            rec += " Improve title/description to boost CTR."
        
        return rec
