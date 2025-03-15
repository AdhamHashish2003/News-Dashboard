import os
import json
import logging
from typing import Dict, List, Any, Optional
import datetime
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Download NLTK resources if not already present
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

class TrendAnalyzer:
    """
    Analyzes trends in classified news data
    """
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def extract_keywords(self, text: str, n: int = 10) -> List[str]:
        """
        Extract most common keywords from text
        
        Args:
            text: Text to analyze
            n: Number of keywords to extract
            
        Returns:
            List of keywords
        """
        # Tokenize text
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords and non-alphabetic tokens
        filtered_tokens = [
            token for token in tokens
            if token.isalpha() and token not in self.stop_words and len(token) > 2
        ]
        
        # Count token frequencies
        token_counts = Counter(filtered_tokens)
        
        # Get most common tokens
        return [token for token, count in token_counts.most_common(n)]
    
    def analyze_category_trends(self, classified_data: Dict[str, Any], 
                               category: str) -> Dict[str, Any]:
        """
        Analyze trends for a specific category
        
        Args:
            classified_data: Classification results
            category: Category to analyze
            
        Returns:
            Trend analysis results
        """
        articles = classified_data.get("classified_articles", [])
        
        # Filter articles by primary category
        category_articles = [
            article for article in articles
            if article.get("classification", {}).get("primary_category") == category
        ]
        
        # Extract all text from relevant sentences
        all_text = ""
        for article in category_articles:
            relevant_sentences = article.get("classification", {}).get("relevant_sentences", {}).get(category, [])
            all_text += " ".join(relevant_sentences)
        
        # Extract keywords
        keywords = self.extract_keywords(all_text, 20)
        
        # Count articles by day
        article_counts_by_day = {}
        for article in category_articles:
            date_str = article.get("published_date", "")
            if date_str:
                try:
                    # Parse date string
                    if 'T' in date_str:
                        # ISO format
                        date = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
                    else:
                        # Try common formats
                        for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']:
                            try:
                                date = datetime.datetime.strptime(date_str, fmt).date()
                                break
                            except ValueError:
                                continue
                        else:
                            continue
                    
                    # Count articles by day
                    day_str = date.isoformat()
                    article_counts_by_day[day_str] = article_counts_by_day.get(day_str, 0) + 1
                
                except Exception as e:
                    logger.error(f"Error parsing date: {e}")
        
        # Calculate average priority score
        avg_priority_score = sum(article.get("priority_score", 0) for article in category_articles) / len(category_articles) if category_articles else 0
        
        return {
            "category": category,
            "article_count": len(category_articles),
            "keywords": keywords,
            "article_counts_by_day": article_counts_by_day,
            "average_priority_score": avg_priority_score
        }
    
    def analyze_all_categories(self, classified_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze trends for all categories
        
        Args:
            classified_data: Classification results
            
        Returns:
            Trend analysis results for all categories
        """
        categories = ["internal_conflict", "external_conflict", "economic_indicators"]
        
        results = {}
        for category in categories:
            results[category] = self.analyze_category_trends(classified_data, category)
        
        return results
    
    def generate_time_series_data(self, classified_data: Dict[str, Any], 
                                days: int = 30) -> Dict[str, Any]:
        """
        Generate time series data for visualization
        
        Args:
            classified_data: Classification results
            days: Number of days to include
            
        Returns:
            Time series data
        """
        articles = classified_data.get("classified_articles", [])
        
        # Calculate date range
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=days)
        
        # Initialize data structure
        date_range = []
        current_date = start_date
        while current_date <= end_date:
            date_range.append(current_date.isoformat())
            current_date += datetime.timedelta(days=1)
        
        time_series = {
            "dates": date_range,
            "internal_conflict": [0] * len(date_range),
            "external_conflict": [0] * len(date_range),
            "economic_indicators": [0] * len(date_range),
            "total": [0] * len(date_range)
        }
        
        # Count articles by day and category
        for article in articles:
            date_str = article.get("published_date", "")
            if date_str:
                try:
                    # Parse date string
                    if 'T' in date_str:
                        # ISO format
                        date = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
                    else:
                        # Try common formats
                        for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']:
                            try:
                                date = datetime.datetime.strptime(date_str, fmt).date()
                                break
                            except ValueError:
                                continue
                        else:
                            continue
                    
                    # Check if date is in range
                    if start_date <= date <= end_date:
                        # Get index in date range
                        index = date_range.index(date.isoformat())
                        
                        # Increment count for category
                        category = article.get("classification", {}).get("primary_category", "uncategorized")
                        if category in time_series:
                            time_series[category][index] += 1
                        
                        # Increment total count
                        time_series["total"][index] += 1
                
                except Exception as e:
                    logger.error(f"Error parsing date: {e}")
        
        return time_series
    
    def analyze_trends(self, classified_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive trend analysis
        
        Args:
            classified_data: Classification results
            
        Returns:
            Trend analysis results
        """
        # Analyze categories
        category_trends = self.analyze_all_categories(classified_data)
        
        # Generate time series data
        time_series = self.generate_time_series_data(classified_data)
        
        # Combine results
        results = {
            "category_trends": category_trends,
            "time_series": time_series,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Save results
        output_file = os.path.join(self.output_dir, f"trend_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Trend analysis results saved to {output_file}")
        
        return results


# Example usage
if __name__ == "__main__":
    # Create trend analyzer
    analyzer = TrendAnalyzer()
    
    # Example classified data file path
    example_data_file = os.path.join(os.path.dirname(__file__), "output", "classification_results_20230615_120000.json")
    
    # Check if example file exists
    if os.path.exists(example_data_file):
        # Load classified data
        with open(example_data_file, 'r') as f:
            classified_data = json.load(f)
        
        # Analyze trends
        trends = analyzer.analyze_trends(classified_data)
        
        print(f"Trend analysis complete. Generated time series data for {len(trends['time_series']['dates'])} days")
    else:
        print(f"Example data file not found: {example_data_file}")
        print("Please run the classification module first to generate classified data files")
