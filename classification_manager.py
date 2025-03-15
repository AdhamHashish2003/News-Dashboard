import os
import json
import logging
from typing import Dict, List, Any, Optional
import datetime
from article_classifier import ArticleClassifier

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ClassificationManager:
    """
    Manager class for classification operations
    """
    def __init__(self):
        self.classifier = ArticleClassifier()
        self.output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process_ingested_data(self, data_file: str) -> Dict[str, Any]:
        """
        Process ingested data from a file
        
        Args:
            data_file: Path to JSON file with ingested data
            
        Returns:
            Dictionary with classification results
        """
        try:
            # Load data
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            # Extract articles and commentary
            articles = data.get("articles", [])
            twitter_commentary = data.get("twitter_commentary", [])
            analyst_commentary = data.get("analyst_commentary", [])
            
            # Classify articles
            classified_articles = self.classifier.classify_articles(articles)
            
            # Classify Twitter commentary
            classified_twitter = self.classifier.classify_articles(twitter_commentary)
            
            # Classify analyst commentary
            classified_analyst = self.classifier.classify_articles(analyst_commentary)
            
            # Generate summaries
            article_summary = self.classifier.generate_classification_summary(classified_articles)
            twitter_summary = self.classifier.generate_classification_summary(classified_twitter)
            analyst_summary = self.classifier.generate_classification_summary(classified_analyst)
            
            # Combine results
            results = {
                "classified_articles": classified_articles,
                "classified_twitter": classified_twitter,
                "classified_analyst": classified_analyst,
                "summaries": {
                    "articles": article_summary,
                    "twitter": twitter_summary,
                    "analyst": analyst_summary
                },
                "metadata": {
                    "classification_time": datetime.datetime.now().isoformat(),
                    "source_file": data_file
                }
            }
            
            # Save results
            output_file = os.path.join(self.output_dir, f"classification_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(f"Classification results saved to {output_file}")
            
            return results
        
        except Exception as e:
            logger.error(f"Error processing ingested data: {e}")
            return {"error": str(e)}
    
    def get_top_articles_by_category(self, classified_data: Dict[str, Any], 
                                    category: str, 
                                    limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top articles for a specific category
        
        Args:
            classified_data: Classification results
            category: Category to filter by (internal_conflict, external_conflict, economic_indicators)
            limit: Maximum number of articles to return
            
        Returns:
            List of top articles for the category
        """
        articles = classified_data.get("classified_articles", [])
        
        # Filter articles by primary category
        category_articles = [
            article for article in articles
            if article.get("classification", {}).get("primary_category") == category
        ]
        
        # Sort by priority score
        category_articles.sort(key=lambda x: x.get("priority_score", 0), reverse=True)
        
        # Return top articles
        return category_articles[:limit]
    
    def get_trending_topics(self, classified_data: Dict[str, Any], 
                           category: str = None,
                           limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get trending topics from classified data
        
        Args:
            classified_data: Classification results
            category: Optional category to filter by
            limit: Maximum number of topics to return
            
        Returns:
            List of trending topics
        """
        articles = classified_data.get("classified_articles", [])
        
        # Filter by category if specified
        if category:
            articles = [
                article for article in articles
                if article.get("classification", {}).get("primary_category") == category
            ]
        
        # Extract relevant sentences
        all_sentences = []
        for article in articles:
            classification = article.get("classification", {})
            relevant_sentences = classification.get("relevant_sentences", {})
            
            if category:
                # Only include sentences for the specified category
                sentences = relevant_sentences.get(category, [])
                for sentence in sentences:
                    all_sentences.append({
                        "sentence": sentence,
                        "article_title": article.get("title", ""),
                        "source": article.get("source", ""),
                        "priority_score": article.get("priority_score", 0)
                    })
            else:
                # Include sentences from all categories
                for cat, sentences in relevant_sentences.items():
                    for sentence in sentences:
                        all_sentences.append({
                            "sentence": sentence,
                            "category": cat,
                            "article_title": article.get("title", ""),
                            "source": article.get("source", ""),
                            "priority_score": article.get("priority_score", 0)
                        })
        
        # Sort by priority score
        all_sentences.sort(key=lambda x: x.get("priority_score", 0), reverse=True)
        
        # Return top sentences as trending topics
        return all_sentences[:limit]
    
    def generate_daily_report(self, classified_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a daily report from classified data
        
        Args:
            classified_data: Classification results
            
        Returns:
            Daily report data
        """
        # Get summaries
        summaries = classified_data.get("summaries", {})
        article_summary = summaries.get("articles", {})
        twitter_summary = summaries.get("twitter", {})
        analyst_summary = summaries.get("analyst", {})
        
        # Get top articles for each category
        internal_conflict_articles = self.get_top_articles_by_category(
            classified_data, "internal_conflict", 5)
        external_conflict_articles = self.get_top_articles_by_category(
            classified_data, "external_conflict", 5)
        economic_indicators_articles = self.get_top_articles_by_category(
            classified_data, "economic_indicators", 5)
        
        # Get trending topics
        trending_topics = self.get_trending_topics(classified_data)
        
        # Create report
        report = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "summary_statistics": {
                "total_articles": article_summary.get("total_articles", 0),
                "category_distribution": article_summary.get("category_counts", {}),
                "average_scores": article_summary.get("average_scores", {})
            },
            "top_articles": {
                "internal_conflict": [
                    {
                        "title": article.get("title", ""),
                        "source": article.get("source", ""),
                        "priority_score": article.get("priority_score", 0),
                        "url": article.get("url", "")
                    }
                    for article in internal_conflict_articles
                ],
                "external_conflict": [
                    {
                        "title": article.get("title", ""),
                        "source": article.get("source", ""),
                        "priority_score": article.get("priority_score", 0),
                        "url": article.get("url", "")
                    }
                    for article in external_conflict_articles
                ],
                "economic_indicators": [
                    {
                        "title": article.get("title", ""),
                        "source": article.get("source", ""),
                        "priority_score": article.get("priority_score", 0),
                        "url": article.get("url", "")
                    }
                    for article in economic_indicators_articles
                ]
            },
            "trending_topics": trending_topics,
            "analyst_insights": [
                {
                    "title": article.get("title", ""),
                    "content": article.get("content", ""),
                    "analyst": article.get("author", ""),
                    "priority_score": article.get("priority_score", 0)
                }
                for article in classified_data.get("classified_analyst", [])[:5]
            ]
        }
        
        # Save report
        output_file = os.path.join(self.output_dir, f"daily_report_{datetime.datetime.now().strftime('%Y%m%d')}.json")
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Daily report saved to {output_file}")
        
        return report


# Example usage
if __name__ == "__main__":
    # Create classification manager
    manager = ClassificationManager()
    
    # Example data file path (would be created by data ingestion module)
    example_data_file = os.path.join(os.path.dirname(__file__), "..", "data_ingestion", "output", "all_data_20230615_120000.json")
    
    # Check if example file exists
    if os.path.exists(example_data_file):
        # Process data
        results = manager.process_ingested_data(example_data_file)
        
        # Generate daily report
        report = manager.generate_daily_report(results)
        
        print(f"Daily report generated with {len(report['top_articles']['internal_conflict'])} internal conflict articles, "
              f"{len(report['top_articles']['external_conflict'])} external conflict articles, and "
              f"{len(report['top_articles']['economic_indicators'])} economic indicators articles")
    else:
        print(f"Example data file not found: {example_data_file}")
        print("Please run the data ingestion module first to generate data files")
