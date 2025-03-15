import os
import json
import logging
from typing import Dict, List, Any, Optional
import datetime
import time
import threading
from queue import Queue

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Processes data from ingestion to database storage
    """
    def __init__(self, db_manager=None, classifier=None, trend_analyzer=None):
        # Import here to avoid circular imports
        if db_manager is None:
            from database_manager import DatabaseManager
            self.db_manager = DatabaseManager()
        else:
            self.db_manager = db_manager
            
        if classifier is None:
            import sys
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'classification'))
            from classification_manager import ClassificationManager
            self.classifier = ClassificationManager()
        else:
            self.classifier = classifier
            
        if trend_analyzer is None:
            import sys
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'classification'))
            from trend_analyzer import TrendAnalyzer
            self.trend_analyzer = TrendAnalyzer()
        else:
            self.trend_analyzer = trend_analyzer
        
        # Create output directory
        self.output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize database
        self.db_manager.create_tables()
    
    def process_data_file(self, data_file: str) -> Dict[str, Any]:
        """
        Process data from a file through the entire pipeline
        
        Args:
            data_file: Path to JSON file with ingested data
            
        Returns:
            Processing results
        """
        try:
            logger.info(f"Processing data file: {data_file}")
            
            # Load data
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            # Extract articles and commentary
            articles = data.get("articles", [])
            twitter_commentary = data.get("twitter_commentary", [])
            analyst_commentary = data.get("analyst_commentary", [])
            
            # Classify data
            logger.info("Classifying articles")
            classified_articles = self.classifier.classify_articles(articles)
            
            logger.info("Classifying Twitter commentary")
            classified_twitter = self.classifier.classify_articles(twitter_commentary)
            
            logger.info("Classifying analyst commentary")
            classified_analyst = self.classifier.classify_articles(analyst_commentary)
            
            # Store in database
            logger.info("Storing articles in database")
            article_ids = []
            for article in classified_articles:
                article_id = self.db_manager.insert_article(article)
                article_ids.append(article_id)
            
            logger.info("Storing Twitter commentary in database")
            twitter_ids = []
            for commentary in classified_twitter:
                commentary_id = self.db_manager.insert_analyst_commentary(commentary)
                twitter_ids.append(commentary_id)
            
            logger.info("Storing analyst commentary in database")
            analyst_ids = []
            for commentary in classified_analyst:
                commentary_id = self.db_manager.insert_analyst_commentary(commentary)
                analyst_ids.append(commentary_id)
            
            # Analyze trends
            logger.info("Analyzing trends")
            classified_data = {
                "classified_articles": classified_articles,
                "classified_twitter": classified_twitter,
                "classified_analyst": classified_analyst
            }
            trends = self.trend_analyzer.analyze_trends(classified_data)
            
            # Store time series data
            logger.info("Storing time series data")
            today = datetime.date.today().isoformat()
            
            # Count articles by category
            category_counts = {
                "internal_conflict": 0,
                "external_conflict": 0,
                "economic_indicators": 0
            }
            
            # Calculate average scores by category
            category_scores = {
                "internal_conflict": [],
                "external_conflict": [],
                "economic_indicators": []
            }
            
            for article in classified_articles:
                category = article.get("classification", {}).get("primary_category")
                if category in category_counts:
                    category_counts[category] += 1
                    
                    score = article.get("priority_score", 0)
                    if score > 0:
                        category_scores[category].append(score)
            
            # Store counts
            for category, count in category_counts.items():
                self.db_manager.insert_time_series_data(f"{category}_count", today, count)
            
            # Store average scores
            for category, scores in category_scores.items():
                if scores:
                    avg_score = sum(scores) / len(scores)
                    self.db_manager.insert_time_series_data(f"{category}_score", today, avg_score)
            
            # Generate daily report
            logger.info("Generating daily report")
            report = self.classifier.generate_daily_report(classified_data)
            
            # Store report
            logger.info("Storing report in database")
            report_id = self.db_manager.insert_report(report)
            
            # Return results
            results = {
                "processed_articles": len(classified_articles),
                "processed_twitter": len(classified_twitter),
                "processed_analyst": len(classified_analyst),
                "article_ids": article_ids,
                "twitter_ids": twitter_ids,
                "analyst_ids": analyst_ids,
                "report_id": report_id,
                "trends": trends,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            # Save results
            output_file = os.path.join(self.output_dir, f"processing_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(f"Processing results saved to {output_file}")
            
            return results
        
        except Exception as e:
            logger.error(f"Error processing data file: {e}")
            return {"error": str(e)}


class ProcessingPipeline:
    """
    Pipeline for processing data from ingestion to storage
    """
    def __init__(self):
        # Import dependencies
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data_ingestion'))
        from ingestion_manager import DataIngestionManager
        
        self.ingestion_manager = DataIngestionManager()
        self.processor = DataProcessor()
        
        # Queue for processing tasks
        self.task_queue = Queue()
        self.processing_thread = None
        self.running = False
    
    def start_pipeline(self) -> None:
        """
        Start the processing pipeline
        """
        if self.running:
            logger.warning("Pipeline is already running")
            return
        
        self.running = True
        self.processing_thread = threading.Thread(target=self._process_queue)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
        logger.info("Processing pipeline started")
    
    def stop_pipeline(self) -> None:
        """
        Stop the processing pipeline
        """
        self.running = False
        if self.processing_thread:
            self.processing_thread.join(timeout=5)
        
        logger.info("Processing pipeline stopped")
    
    def _process_queue(self) -> None:
        """
        Process tasks from the queue
        """
        while self.running:
            try:
                if not self.task_queue.empty():
                    task = self.task_queue.get()
                    
                    if task["type"] == "ingest_and_process":
                        self._ingest_and_process(task["query"])
                    elif task["type"] == "process_file":
                        self.processor.process_data_file(task["file_path"])
                    
                    self.task_queue.task_done()
                else:
                    # Sleep to avoid high CPU usage
                    time.sleep(1)
            
            except Exception as e:
                logger.error(f"Error in processing thread: {e}")
    
    def _ingest_and_process(self, query: str) -> None:
        """
        Ingest data and process it
        
        Args:
            query: Query for data ingestion
        """
        try:
            # Ingest data
            logger.info(f"Ingesting data for query: {query}")
            data = self.ingestion_manager.ingest_data(query=query)
            
            # Save data to file
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            data_file = os.path.join(self.processor.output_dir, f"ingested_data_{timestamp}.json")
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Process data
            logger.info(f"Processing ingested data from {data_file}")
            self.processor.process_data_file(data_file)
        
        except Exception as e:
            logger.error(f"Error in ingest_and_process: {e}")
    
    def schedule_ingestion(self, query: str) -> None:
        """
        Schedule data ingestion and processing
        
        Args:
            query: Query for data ingestion
        """
        self.task_queue.put({
            "type": "ingest_and_process",
            "query": query
        })
        
        logger.info(f"Scheduled ingestion for query: {query}")
    
    def schedule_file_processing(self, file_path: str) -> None:
        """
        Schedule processing of a data file
        
        Args:
            file_path: Path to data file
        """
        self.task_queue.put({
            "type": "process_file",
            "file_path": file_path
        })
        
        logger.info(f"Scheduled processing of file: {file_path}")
    
    def run_scheduled_pipeline(self, interval_hours: int = 24) -> None:
        """
        Run the pipeline on a schedule
        
        Args:
            interval_hours: Hours between pipeline runs
        """
        # Start the pipeline
        self.start_pipeline()
        
        # Define queries
        queries = [
            "inflation OR recession OR \"interest rates\"",
            "\"internal conflict\" OR \"civil unrest\" OR protests",
            "\"external conflict\" OR \"trade war\" OR \"geopolitical tension\"",
            "\"Ray Dalio\" OR \"New World Order\" OR \"changing world order\""
        ]
        
        # Schedule initial ingestion
        for query in queries:
            self.schedule_ingestion(query)
        
        logger.info(f"Scheduled pipeline to run every {interval_hours} hours")
        
        # In a real implementation, this would use a scheduler like Celery
        # For demonstration, we'll just run once and then stop
        try:
            # Wait for all tasks to complete
            self.task_queue.join()
            
            # Stop the pipeline
            self.stop_pipeline()
            
            logger.info("Scheduled pipeline run completed")
        
        except KeyboardInterrupt:
            logger.info("Pipeline interrupted by user")
            self.stop_pipeline()


# Example usage
if __name__ == "__main__":
    # Create processing pipeline
    pipeline = ProcessingPipeline()
    
    # Run scheduled pipeline
    pipeline.run_scheduled_pipeline()
