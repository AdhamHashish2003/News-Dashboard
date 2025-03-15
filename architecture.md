# System Architecture Design

This document outlines the detailed architecture for the Ray Dalio-inspired "New World Order" News Dashboard.

## 1. Data Ingestion Architecture

### News API Integration
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  News API   │───▶│ API Adapter │───▶│ Data Parser │
└─────────────┘    └─────────────┘    └─────────────┘
                                             │
                                             ▼
                                      ┌─────────────┐
                                      │ Data Storage│
                                      └─────────────┘
```

### Components:
- **API Adapter**: Handles authentication and rate limiting for various news sources
- **Data Parser**: Extracts relevant fields from API responses
- **Storage Interface**: Standardizes data format before database insertion

### Supported Sources:
- NewsAPI (primary source)
- Google News RSS feeds
- Financial Times API
- Twitter API (for analyst commentary)
- WSJ RSS feeds

## 2. Classification Engine

### Ray Dalio Framework Implementation
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Raw Article │───▶│ Text Analysis│───▶│ Classification│
└─────────────┘    └─────────────┘    └─────────────┘
                          │                   │
                          ▼                   ▼
                   ┌─────────────┐    ┌─────────────┐
                   │Entity Extract│    │Priority Score│
                   └─────────────┘    └─────────────┘
```

### Classification Categories:
- **Internal Conflict**: Civil unrest, domestic policy disputes, social tensions
- **External Conflict**: International tensions, trade disputes, military conflicts
- **Economic Indicators**: Interest rates, inflation, GDP, unemployment
- **Analyst Commentary**: Expert opinions and predictions

### Scoring Algorithm:
- Source credibility weight: 0.3
- Recency weight: 0.25
- Relevance to Dalio's framework: 0.3
- Geographic importance: 0.15

## 3. Database Architecture

### Schema Design
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Articles   │────▶│ Categories  │◀────│  Analysts   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Metrics   │────▶│  TimeSeries │◀────│    Tags     │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Database Tables:
- **Articles**: id, title, content, source, url, published_date, priority_score
- **Categories**: id, name, description, parent_category
- **ArticleCategories**: article_id, category_id, confidence_score
- **Analysts**: id, name, organization, expertise, credibility_score
- **AnalystCommentary**: id, analyst_id, content, date, article_id
- **Metrics**: id, name, description, calculation_method
- **TimeSeries**: metric_id, date, value

## 4. Frontend Architecture

### Component Structure
```
┌─────────────────────────────────────────────────┐
│                  App Container                  │
├─────────────┬─────────────┬────────────────────┤
│  Navigation │  Dashboard  │  Settings Panel    │
├─────────────┴─────────────┴────────────────────┤
│                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────┐  │
│  │ News Feed   │  │ Conflict    │  │ Analyst │  │
│  │ Component   │  │ Charts      │  │ Quotes  │  │
│  └─────────────┘  └─────────────┘  └─────────┘  │
│                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────┐  │
│  │ Economic    │  │ Geographic  │  │ Search/ │  │
│  │ Indicators  │  │ Heatmap     │  │ Filter  │  │
│  └─────────────┘  └─────────────┘  └─────────┘  │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Key UI Components:
- **News Feed**: Prioritized list of articles with filtering options
- **Conflict Charts**: Time-series visualization of internal/external conflict mentions
- **Analyst Quotes**: Recent commentary from tracked analysts
- **Economic Indicators**: Charts of key economic metrics
- **Geographic Heatmap**: Visual representation of global conflict hotspots
- **Search/Filter Panel**: Advanced query interface for customized views

## 5. ChatGPT Integration

### Integration Architecture
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ News Article│───▶│ ChatGPT API │───▶│ AI Analysis │
└─────────────┘    └─────────────┘    └─────────────┘
                          │                  │
                          ▼                  ▼
                   ┌─────────────┐    ┌─────────────┐
                   │ Summaries   │    │ Predictions │
                   └─────────────┘    └─────────────┘
```

### ChatGPT Features:
- **Article Summarization**: Condense long articles into key points
- **Trend Analysis**: Identify patterns across multiple news sources
- **Prediction Generation**: Create forecasts based on current news
- **Framework Alignment**: Map news to Ray Dalio's economic principles
- **Sentiment Analysis**: Gauge emotional tone of coverage

## 6. Data Processing Pipeline

### ETL Workflow
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Extraction  │───▶│Transformation│───▶│  Loading    │
└─────────────┘    └─────────────┘    └─────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Scheduling  │◀───│  Monitoring │◀───│   Alerts    │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Processing Components:
- **Batch Processing**: Daily aggregation of news and metrics
- **Real-time Updates**: Breaking news detection and immediate classification
- **Trend Calculation**: Rolling averages and statistical analysis
- **Alert Generation**: Notification system for significant developments

## 7. Technology Stack Details

### Backend:
- Python 3.9+
- FastAPI for API endpoints
- Celery for task scheduling
- NLTK and spaCy for NLP
- OpenAI API for ChatGPT integration

### Database:
- MongoDB for article storage
- TimescaleDB for time-series data
- Redis for caching

### Frontend:
- React 18
- Redux for state management
- D3.js and Plotly for visualizations
- Material UI for components
- Mapbox for geographic visualization

### Deployment:
- Docker containers
- Docker Compose for local development
- GitHub Actions for CI/CD
