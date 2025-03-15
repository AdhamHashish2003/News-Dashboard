# Ray Dalio's "New World Order" News Dashboard

## Project Overview

This project implements a comprehensive news dashboard based on Ray Dalio's "New World Order" framework, focusing on tracking internal conflicts, external conflicts, and economic indicators. The dashboard aggregates news from various sources, classifies articles using AI, and provides visualizations and insights to help users understand global trends through Ray Dalio's perspective.

## Key Features

- **News Aggregation**: Collects articles from multiple sources and APIs
- **Analyst Commentary Tracking**: Monitors insights from prominent economists and analysts
- **AI-Powered Classification**: Uses ChatGPT to categorize content based on Ray Dalio's framework
- **Interactive Dashboard**: Visualizes trends, hotspots, and priority news
- **Daily Reports**: Generates AI-summarized reports of key developments

## System Architecture

The system is built with a modular architecture consisting of:

1. **Data Ingestion Layer**: Collects news and analyst commentary
2. **Classification Engine**: Categorizes content using Ray Dalio's framework
3. **Database & Processing Pipeline**: Stores and processes data
4. **Frontend Dashboard**: Visualizes insights with interactive components
5. **ChatGPT Integration**: Enhances analysis with AI-powered insights

## Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js 14+
- SQLite
- OpenAI API key (for ChatGPT integration)

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ray-dalio-dashboard.git
cd ray-dalio-dashboard
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install backend dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export OPENAI_API_KEY="your_openai_api_key"
export NEWS_API_KEY="your_news_api_key"
```

5. Initialize the database:
```bash
python -m database.database_manager
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install frontend dependencies:
```bash
npm install
```

3. Build the frontend:
```bash
npm run build
```

## Running the Application

### Start the Backend

```bash
python app.py
```

### Start the Frontend Development Server

```bash
cd frontend
npm start
```

The application will be available at http://localhost:3000

## Usage Guide

### Dashboard Navigation

The dashboard is organized into five main tabs:

1. **Overview**: Shows a summary of all categories with priority news
2. **Internal Conflict**: Focuses on domestic unrest, political polarization, etc.
3. **External Conflict**: Highlights international tensions, trade disputes, etc.
4. **Economic Indicators**: Tracks inflation, interest rates, debt levels, etc.
5. **Analyst Insights**: Features commentary from prominent economists

### Search & Filtering

Use the search bar at the top to find specific topics, and use the filters to:
- Select specific categories
- Choose time periods
- Filter by region
- Set custom date ranges

### Interactive Features

- Click on map hotspots to see conflict details
- Hover over chart data points for specific values
- Sort news by priority score or recency
- View analyst quotes with their organizational affiliations

## Component Documentation

### Data Ingestion

The data ingestion module collects news from various sources:

- `news_collector.py`: Fetches articles from news APIs
- `analyst_tracker.py`: Monitors commentary from economists and analysts
- `ingestion_manager.py`: Coordinates the ingestion process

### Classification

The classification module categorizes content based on Ray Dalio's framework:

- `article_classifier.py`: Classifies articles into categories
- `classification_manager.py`: Manages the classification workflow
- `trend_analyzer.py`: Analyzes trends in classified data

### Database

The database module stores and processes the data:

- `database_manager.py`: Handles database operations
- `data_processor.py`: Processes data through the pipeline

### Frontend

The frontend is built with React and includes:

- `Dashboard.js`: Main dashboard component
- `NewsFeed.js`: Displays prioritized news articles
- `ConflictCharts.js`: Visualizes conflict trends
- `AnalystQuotes.js`: Shows analyst commentary
- `EconomicIndicators.js`: Displays economic data
- `GeographicMap.js`: Shows global conflict hotspots
- `SearchFilter.js`: Provides filtering capabilities

### ChatGPT Integration

The ChatGPT integration enhances analysis:

- `chatgpt_analyzer.py`: Interfaces with OpenAI API
- `news_analysis_manager.py`: Manages AI-powered analysis

## Customization

### Adding New Categories

To add new categories beyond internal conflict, external conflict, and economic indicators:

1. Add the category to the `Categories` table in `database_manager.py`
2. Update the classification logic in `article_classifier.py`
3. Add a new tab in `Dashboard.js`
4. Create visualizations for the new category

### Modifying Priority Scoring

The priority scoring algorithm can be adjusted in `article_classifier.py` by modifying the weights assigned to different factors:

- Source credibility
- Recency
- Keyword relevance
- Entity importance

### Adding New Data Sources

To add new data sources:

1. Create a new collector in the data_ingestion module
2. Update `ingestion_manager.py` to include the new source
3. Adjust the data processing pipeline as needed

## Testing

Run the test suite to verify all components:

```bash
python -m unittest discover tests
```

The test suite includes:

- Unit tests for each component
- Integration tests for the pipeline
- End-to-end workflow tests

## Future Enhancements

Potential areas for future development:

1. **Advanced NLP**: Implement more sophisticated text analysis
2. **Real-time Updates**: Add WebSocket support for live updates
3. **Predictive Analytics**: Forecast potential developments
4. **Mobile App**: Create a companion mobile application
5. **Personalization**: Allow users to customize their dashboard view

## Acknowledgments

- Ray Dalio for his "Changing World Order" framework
- OpenAI for the ChatGPT API
- Various news sources and APIs used in the project

## License

This project is licensed under the MIT License - see the LICENSE file for details.
