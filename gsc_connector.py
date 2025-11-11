"""
Google Search Console Sentiment Analysis Tool

This module provides functionality to connect to Google Search Console API
and retrieve search analytics data for sentiment analysis.
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle


class GSCConnector:
    """Handle Google Search Console API connections and data retrieval."""
    
    SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
    
    def __init__(self, credentials_path: str = 'credentials.json'):
        """
        Initialize GSC Connector.
        
        Args:
            credentials_path: Path to OAuth2 credentials JSON file
        """
        self.credentials_path = credentials_path
        self.service = None
        self.creds = None
        
    def authenticate(self):
        """Authenticate with Google Search Console API."""
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Credentials file not found at {self.credentials_path}. "
                        "Please download OAuth2 credentials from Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
        
        self.service = build('searchconsole', 'v1', credentials=self.creds)
        return self.service
    
    def list_sites(self) -> List[str]:
        """
        List all sites available in Search Console.
        
        Returns:
            List of site URLs
        """
        if not self.service:
            self.authenticate()
        
        site_list = self.service.sites().list().execute()
        return [site['siteUrl'] for site in site_list.get('siteEntry', [])]
    
    def get_search_analytics(
        self,
        site_url: str,
        start_date: str,
        end_date: str,
        dimensions: List[str] = None,
        row_limit: int = 25000
    ) -> Dict:
        """
        Retrieve search analytics data from GSC.
        
        Args:
            site_url: The site URL to query
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            dimensions: List of dimensions (query, page, country, device, searchAppearance)
            row_limit: Maximum number of rows to return
            
        Returns:
            Dictionary containing search analytics data
        """
        if not self.service:
            self.authenticate()
        
        if dimensions is None:
            dimensions = ['query', 'page']
        
        request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': dimensions,
            'rowLimit': row_limit
        }
        
        response = self.service.searchanalytics().query(
            siteUrl=site_url,
            body=request
        ).execute()
        
        return response
    
    def get_recent_data(
        self,
        site_url: str,
        days: int = 30,
        dimensions: List[str] = None
    ) -> Dict:
        """
        Get search analytics data for recent days.
        
        Args:
            site_url: The site URL to query
            days: Number of days to look back
            dimensions: List of dimensions to include
            
        Returns:
            Dictionary containing search analytics data
        """
        end_date = datetime.now() - timedelta(days=3)  # GSC data has ~3 day delay
        start_date = end_date - timedelta(days=days)
        
        return self.get_search_analytics(
            site_url=site_url,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            dimensions=dimensions
        )
