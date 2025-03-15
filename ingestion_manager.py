import os
import json
import logging
from typing import Dict, List, Any, Optional
import datetime
from news_collector import DataCollector
from analyst_tracker import AnalystTracker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataIngestionManager:
    """
    Main class to manage data ingestion from all sources
    """
    def __init__(self, newsapi_key: Optional[str] = None):
        self.data_collector = DataCollector(newsapi_key=newsapi_key)
        self.analyst_tracker = AnalystTracker()
        self.output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def ingest_data(self, 
                   query: Optional[str] = None,
                   from_date: Optional[str] = None,
                   to_date: Optional[str] = None,
                   save_output: bool = True) -> Dict[str, Any]:
        """
        Ingest data from all sources
        
        Args:
            query: Keywords to search for
            from_date: Start date for search
            to_date: End date for search
            save_output: Whether to save output to files
            
        Returns:
            Dictionary with all collected data
        """
        logger.info("Starting data ingestion process")
        
        # Collect news articles
        logger.info("Collecting news articles")
        news_data = self.data_collector.collect_all_data(query, from_date, to_date)
        
        # Collect analyst commentary
        logger.info("Collecting analyst commentary")
        analyst_commentary = self.analyst_tracker.collect_all_commentary()
        
        # Combine all data
        all_data = {
            "articles": news_data["articles"],
            "twitter_commentary": news_data["analyst_commentary"],
            "analyst_commentary": analyst_commentary,
            "metadata": {
                "ingestion_time": datetime.datetime.now().isoformat(),
                "query": query,
                "from_date": from_date,
                "to_date": to_date
            }
        }
        
        # Save output if requested
        if save_output:
            self._save_data(all_data)
        
        logger.info(f"Data ingestion complete. Collected {len(all_data['articles'])} articles, "
                   f"{len(all_data['twitter_commentary'])} tweets, and "
                   f"{len(all_data['analyst_commentary'])} analyst comments")
        
        return all_data
    
    def _save_data(self, data: Dict[str, Any]) -> None:
        """
        Save collected data to files
        
        Args:
            data: Data to save
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save articles
        articles_file = os.path.join(self.output_dir, f"articles_{timestamp}.json")
        with open(articles_file, "w") as f:
            json.dump(data["articles"], f, indent=2)
        logger.info(f"Saved {len(data['articles'])} articles to {articles_file}")
        
        # Save Twitter commentary
        twitter_file = os.path.join(self.output_dir, f"twitter_{timestamp}.json")
        with open(twitter_file, "w") as f:
            json.dump(data["twitter_commentary"], f, indent=2)
        logger.info(f"Saved {len(data['twitter_commentary'])} tweets to {twitter_file}")
        
        # Save analyst commentary
        analyst_file = os.path.join(self.output_dir, f"analyst_{timestamp}.json")
        with open(analyst_file, "w") as f:
            json.dump(data["analyst_commentary"], f, indent=2)
        logger.info(f"Saved {len(data['analyst_commentary'])} analyst comments to {analyst_file}")
        
        # Save combined data
        combined_file = os.path.join(self.output_dir, f"all_data_{timestamp}.json")
        with open(combined_file, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved combined data to {combined_file}")
    
    def run_scheduled_ingestion(self, 
                              interval_hours: int = 24,
                              queries: List[str] = None) -> None:
        """
        Run data ingestion on a schedule
        
        Args:
            interval_hours: Hours between ingestion runs
            queries: List of queries to search for
        """
        if queries is None:
            queries = [
                "inflation OR recession OR \"interest rates\"",
                "\"internal conflict\" OR \"civil unrest\" OR protests",
                "\"external conflict\" OR \"trade war\" OR \"geopolitical tension\"",
                "\"Ray Dalio\" OR \"New World Order\" OR \"changing world order\""
            ]
        
        logger.info(f"Starting scheduled ingestion every {interval_hours} hours")
        logger.info(f"Queries: {queries}")
        
        # In a real implementation, this would use a scheduler like Celery
        # For demonstration, we'll just run once
        for query in queries:
            logger.info(f"Running ingestion for query: {query}")
            self.ingest_data(query=query)
        
        logger.info("Scheduled ingestion complete")


# Example usage
if __name__ == "__main__":
    # Create data ingestion manager
    manager = DataIngestionManager()
    
    # Run data ingestion
    manager.run_scheduled_ingestion()
