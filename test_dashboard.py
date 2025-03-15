import os
import json
import logging
import unittest
from unittest.mock import patch, MagicMock
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestDashboardComponents(unittest.TestCase):
    """
    Test suite for Ray Dalio Dashboard components
    """
    
    def setUp(self):
        """Set up test environment"""
        # Create test output directory
        self.test_output_dir = os.path.join(os.path.dirname(__file__), "test_output")
        os.makedirs(self.test_output_dir, exist_ok=True)
    
    def test_data_ingestion(self):
        """Test data ingestion module"""
        from data_ingestion.news_collector import NewsCollector
        from data_ingestion.analyst_tracker import AnalystTracker
        
        # Test NewsCollector
        with patch('data_ingestion.news_collector.requests.get') as mock_get:
            # Mock response for news API
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'articles': [
                    {
                        'title': 'Test Article',
                        'description': 'Test Description',
                        'url': 'https://example.com/article1',
                        'publishedAt': '2023-06-15T10:30:00Z',
                        'source': {'name': 'Test Source'}
                    }
                ]
            }
            mock_get.return_value = mock_response
            
            # Create NewsCollector and fetch news
            collector = NewsCollector(api_key='test_key')
            articles = collector.fetch_news(query='test', max_results=1)
            
            # Verify results
            self.assertEqual(len(articles), 1)
            self.assertEqual(articles[0]['title'], 'Test Article')
            
        # Test AnalystTracker
        with patch('data_ingestion.analyst_tracker.requests.get') as mock_get:
            # Mock response for Twitter API
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'data': [
                    {
                        'text': 'Test Tweet',
                        'created_at': '2023-06-15T10:30:00Z',
                        'author_id': '12345'
                    }
                ],
                'includes': {
                    'users': [
                        {
                            'id': '12345',
                            'name': 'Test Analyst',
                            'username': 'testanalyst'
                        }
                    ]
                }
            }
            mock_get.return_value = mock_response
            
            # Create AnalystTracker and fetch tweets
            tracker = AnalystTracker(api_key='test_key')
            tweets = tracker.fetch_analyst_tweets(analyst_username='testanalyst', max_results=1)
            
            # Verify results
            self.assertEqual(len(tweets), 1)
            self.assertEqual(tweets[0]['text'], 'Test Tweet')
            self.assertEqual(tweets[0]['analyst_name'], 'Test Analyst')
    
    def test_classification(self):
        """Test classification module"""
        from classification.article_classifier import ArticleClassifier
        
        # Create test article
        test_article = {
            'title': 'Global Trade Tensions Escalate as US and China Impose New Tariffs',
            'content': 'Trade tensions between the United States and China escalated today as both countries announced new tariffs on each other\'s goods.'
        }
        
        # Create classifier and classify article
        classifier = ArticleClassifier()
        classified_article = classifier.classify_article(test_article)
        
        # Verify results
        self.assertIn('classification', classified_article)
        self.assertIn('primary_category', classified_article['classification'])
        self.assertIn('priority_score', classified_article)
        
        # Test with different article types
        internal_conflict_article = {
            'title': 'Protests Erupt in Major Cities Over Economic Inequality',
            'content': 'Thousands took to the streets in several major cities today, protesting growing economic inequality and government policies.'
        }
        
        economic_article = {
            'title': 'Central Banks Signal Shift in Monetary Policy Amid Inflation Concerns',
            'content': 'Several central banks have signaled a potential shift in monetary policy as inflation concerns grow in major economies.'
        }
        
        # Classify articles
        internal_result = classifier.classify_article(internal_conflict_article)
        economic_result = classifier.classify_article(economic_article)
        
        # Verify different classifications
        self.assertEqual(internal_result['classification']['primary_category'], 'internal_conflict')
        self.assertEqual(economic_result['classification']['primary_category'], 'economic_indicators')
    
    def test_database(self):
        """Test database module"""
        from database.database_manager import DatabaseManager
        import sqlite3
        import os
        
        # Create test database path
        test_db_path = os.path.join(self.test_output_dir, "test_database.db")
        
        # Remove test database if it exists
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
        
        # Create database manager
        db_manager = DatabaseManager(db_path=test_db_path)
        
        # Create tables
        db_manager.create_tables()
        
        # Verify database was created
        self.assertTrue(os.path.exists(test_db_path))
        
        # Test inserting and retrieving an article
        test_article = {
            'title': 'Test Article',
            'content': 'Test Content',
            'url': 'https://example.com/article1',
            'published_date': '2023-06-15T10:30:00Z',
            'source': 'Test Source',
            'priority_score': 75.0,
            'classification': {
                'primary_category': 'external_conflict',
                'secondary_category': 'economic_indicators'
            }
        }
        
        # Insert article
        article_id = db_manager.insert_article(test_article)
        
        # Verify article was inserted
        self.assertIsNotNone(article_id)
        
        # Retrieve article by category
        articles = db_manager.get_articles_by_category('external_conflict', limit=1)
        
        # Verify article was retrieved
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]['title'], 'Test Article')
    
    def test_chatgpt_integration(self):
        """Test ChatGPT integration module"""
        from chatgpt_integration.chatgpt_analyzer import ChatGPTIntegration
        
        # Mock ChatGPT API response
        mock_response = {
            'choices': [
                {
                    'message': {
                        'content': json.dumps({
                            'summary': 'Test summary',
                            'classification': {
                                'primary_category': 'external_conflict',
                                'confidence': 85
                            },
                            'entities': ['US', 'China'],
                            'implications': 'Test implications',
                            'priority_score': 75,
                            'ray_dalio_perspective': 'Test perspective'
                        })
                    }
                }
            ]
        }
        
        # Create test article
        test_article = {
            'title': 'Test Article',
            'content': 'Test Content'
        }
        
        # Test article analysis
        with patch.object(ChatGPTIntegration, '_call_chatgpt_api', return_value=mock_response):
            chatgpt = ChatGPTIntegration(api_key='test_key')
            analyzed_article = chatgpt.analyze_article(test_article)
            
            # Verify results
            self.assertIn('analysis', analyzed_article)
            self.assertEqual(analyzed_article['analysis']['summary'], 'Test summary')
            self.assertEqual(analyzed_article['analysis']['classification']['primary_category'], 'external_conflict')
    
    def test_frontend_components(self):
        """
        Test frontend components (simplified test)
        
        Note: In a real implementation, we would use a frontend testing framework
        like Jest or React Testing Library. This is a simplified test to check
        that the files exist and have the expected content.
        """
        # Check that frontend files exist
        frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
        
        # List of expected files
        expected_files = [
            os.path.join(frontend_dir, "src", "App.js"),
            os.path.join(frontend_dir, "src", "components", "Dashboard.js"),
            os.path.join(frontend_dir, "src", "components", "NewsFeed.js"),
            os.path.join(frontend_dir, "src", "components", "ConflictCharts.js"),
            os.path.join(frontend_dir, "src", "components", "AnalystQuotes.js"),
            os.path.join(frontend_dir, "src", "components", "EconomicIndicators.js"),
            os.path.join(frontend_dir, "src", "components", "GeographicMap.js"),
            os.path.join(frontend_dir, "src", "components", "SearchFilter.js")
        ]
        
        # Check that each file exists
        for file_path in expected_files:
            self.assertTrue(os.path.exists(file_path), f"File {file_path} does not exist")
            
            # Check that file has content
            with open(file_path, 'r') as f:
                content = f.read()
                self.assertGreater(len(content), 0, f"File {file_path} is empty")
    
    def test_end_to_end(self):
        """
        Test end-to-end workflow (simplified)
        
        This test simulates the entire workflow from data ingestion to frontend rendering.
        In a real implementation, this would be more comprehensive and include actual API calls.
        """
        # Import necessary modules
        from data_ingestion.ingestion_manager import DataIngestionManager
        from classification.classification_manager import ClassificationManager
        from database.data_processor import DataProcessor
        from chatgpt_integration.news_analysis_manager import NewsAnalysisManager
        
        # Mock data for testing
        test_data = {
            'articles': [
                {
                    'title': 'Global Trade Tensions Escalate as US and China Impose New Tariffs',
                    'content': 'Trade tensions between the United States and China escalated today as both countries announced new tariffs on each other\'s goods.',
                    'source': 'Financial Times',
                    'published_date': '2023-06-15T10:30:00Z'
                },
                {
                    'title': 'Protests Erupt in Major Cities Over Economic Inequality',
                    'content': 'Thousands took to the streets in several major cities today, protesting growing economic inequality and government policies.',
                    'source': 'The New York Times',
                    'published_date': '2023-06-14T14:45:00Z'
                }
            ],
            'analyst_commentary': [
                {
                    'content': 'The current trade tensions represent a fundamental shift in the global economic order.',
                    'analyst_name': 'Ray Dalio',
                    'organization': 'Bridgewater Associates',
                    'date': '2023-06-15T08:30:00Z'
                }
            ]
        }
        
        # Create test data file
        test_data_file = os.path.join(self.test_output_dir, "test_data.json")
        with open(test_data_file, 'w') as f:
            json.dump(test_data, f)
        
        # Test data ingestion (mocked)
        with patch.object(DataIngestionManager, 'ingest_data', return_value=test_data):
            ingestion_manager = DataIngestionManager()
            ingested_data = ingestion_manager.ingest_data(query='test')
            
            # Verify ingested data
            self.assertEqual(len(ingested_data['articles']), 2)
            self.assertEqual(len(ingested_data['analyst_commentary']), 1)
        
        # Test classification (mocked)
        with patch.object(ClassificationManager, 'classify_articles', return_value=test_data['articles']):
            classification_manager = ClassificationManager()
            classified_articles = classification_manager.classify_articles(test_data['articles'])
            
            # Verify classified articles
            self.assertEqual(len(classified_articles), 2)
        
        # Test data processing (mocked)
        with patch.object(DataProcessor, 'process_data_file', return_value={'processed_articles': 2}):
            data_processor = DataProcessor()
            processing_results = data_processor.process_data_file(test_data_file)
            
            # Verify processing results
            self.assertEqual(processing_results['processed_articles'], 2)
        
        # Test ChatGPT analysis (mocked)
        with patch.object(NewsAnalysisManager, 'analyze_articles', return_value=test_data['articles']):
            news_analysis_manager = NewsAnalysisManager()
            analyzed_articles = news_analysis_manager.analyze_articles(test_data['articles'])
            
            # Verify analyzed articles
            self.assertEqual(len(analyzed_articles), 2)
        
        # Test report generation (mocked)
        with patch.object(NewsAnalysisManager, 'generate_daily_report', return_value={'date': '2023-06-15'}):
            report = news_analysis_manager.generate_daily_report('2023-06-15')
            
            # Verify report
            self.assertEqual(report['date'], '2023-06-15')
        
        logger.info("End-to-end test completed successfully")


if __name__ == '__main__':
    unittest.main()
