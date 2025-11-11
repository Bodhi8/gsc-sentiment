# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-11

### Added
- Initial release of GSC Sentiment Analyzer
- Google Search Console data fetching via API
- Sentiment analysis using VADER and TextBlob
- Entity extraction using spaCy for AI citation optimization
- Performance scoring system combining clicks, impressions, CTR, and position
- Automated identification of content strengths and weaknesses
- Comprehensive text-based insights reporting
- CSV export functionality for all analysis results
- Static visualizations using Matplotlib and Seaborn
- Interactive dashboard using Plotly
- Example scripts demonstrating various use cases
- Complete API documentation
- User guide with best practices
- Setup script for easy installation
- Unit tests for core functionality
- Support for multiple dimensions (query, page, country, device)
- Comparative analysis across time periods
- Country-specific analysis
- Configurable via environment variables

### Features
- **Sentiment Analysis**: Dual-method approach using VADER (web-optimized) and TextBlob
- **Entity Recognition**: Named entity extraction for people, organizations, products, locations
- **Performance Metrics**: Weighted scoring system for overall query performance
- **Strengths Identification**: Automatic detection of high-performing positive content
- **Weaknesses Identification**: Automatic detection of underperforming or negative content
- **AI Citation Optimization**: Entity analysis for improving visibility in AI systems
- **Visualization Suite**: Multiple chart types for data exploration
- **Interactive Dashboard**: HTML-based dashboard for dynamic exploration
- **Flexible Configuration**: Easy setup via .env file
- **Comprehensive Documentation**: README, API reference, and user guide

### Technical Details
- Python 3.8+ support
- Google Search Console API integration
- NLP processing with VADER, TextBlob, and spaCy
- Data manipulation with Pandas
- Visualization with Matplotlib, Seaborn, and Plotly
- Modular architecture for easy extension
- Type hints for better code clarity
- Error handling and fallback mechanisms

### Documentation
- README with installation and basic usage
- API_REFERENCE.md with complete method documentation
- GUIDE.md with in-depth explanations and best practices
- Example scripts for common use cases
- Inline code documentation

### Testing
- Unit tests for core sentiment analysis functions
- Tests for data processing and categorization
- Mock-based testing for API interactions
- Edge case testing for special characters and empty inputs
