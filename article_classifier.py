import os
import json
import logging
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from typing import Dict, List, Any, Optional, Tuple
import datetime

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

class DalioFrameworkClassifier:
    """
    Classifier based on Ray Dalio's "New World Order" framework
    """
    def __init__(self):
        # Keywords for internal conflict classification
        self.internal_conflict_keywords = [
            "civil unrest", "protest", "domestic policy", "wealth inequality",
            "political polarization", "social tension", "class struggle",
            "income gap", "wealth gap", "social divide", "domestic conflict",
            "internal struggle", "civil disobedience", "political divide",
            "social unrest", "populism", "nationalism", "domestic politics",
            "culture war", "identity politics", "political instability"
        ]
        
        # Keywords for external conflict classification
        self.external_conflict_keywords = [
            "international tension", "tariff", "trade war", "border dispute",
            "geopolitical risk", "military conflict", "diplomatic crisis",
            "foreign policy", "international relation", "global competition",
            "economic warfare", "currency war", "territorial dispute",
            "international sanction", "global power", "superpower competition",
            "military buildup", "alliance", "proxy war", "cold war",
            "international order", "global governance"
        ]
        
        # Keywords for economic indicators
        self.economic_indicators_keywords = [
            "interest rate", "inflation", "gdp", "unemployment", "debt level",
            "monetary policy", "fiscal policy", "central bank", "federal reserve",
            "economic growth", "recession", "economic cycle", "market crash",
            "financial crisis", "credit cycle", "debt cycle", "productivity",
            "economic output", "consumer spending", "business investment",
            "economic indicator", "economic data", "economic report"
        ]
        
        # Compile regex patterns for more efficient matching
        self.internal_conflict_patterns = self._compile_patterns(self.internal_conflict_keywords)
        self.external_conflict_patterns = self._compile_patterns(self.external_conflict_keywords)
        self.economic_indicators_patterns = self._compile_patterns(self.economic_indicators_keywords)
        
        # Load stopwords
        self.stop_words = set(stopwords.words('english'))
    
    def _compile_patterns(self, keywords: List[str]) -> List[re.Pattern]:
        """
        Compile regex patterns for keywords
        
        Args:
            keywords: List of keywords or phrases
            
        Returns:
            List of compiled regex patterns
        """
        patterns = []
        for keyword in keywords:
            # Create pattern that matches whole words or phrases
            if " " in keyword:
                # For phrases, match the exact phrase
                pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
            else:
                # For single words, match word boundaries
                pattern = re.compile(r'\b' + re.escape(keyword) + r'[a-zA-Z]*\b', re.IGNORECASE)
            patterns.append(pattern)
        return patterns
    
    def classify_text(self, text: str) -> Dict[str, Any]:
        """
        Classify text according to Ray Dalio's framework
        
        Args:
            text: Text to classify
            
        Returns:
            Dictionary with classification results
        """
        # Preprocess text
        text = text.lower()
        
        # Count matches for each category
        internal_conflict_count = self._count_matches(text, self.internal_conflict_patterns)
        external_conflict_count = self._count_matches(text, self.external_conflict_patterns)
        economic_indicators_count = self._count_matches(text, self.economic_indicators_patterns)
        
        # Calculate total matches
        total_matches = internal_conflict_count + external_conflict_count + economic_indicators_count
        
        # Calculate confidence scores (as percentages of total matches)
        if total_matches > 0:
            internal_conflict_score = (internal_conflict_count / total_matches) * 100
            external_conflict_score = (external_conflict_count / total_matches) * 100
            economic_indicators_score = (economic_indicators_count / total_matches) * 100
        else:
            internal_conflict_score = 0
            external_conflict_score = 0
            economic_indicators_score = 0
        
        # Determine primary and secondary categories
        categories = [
            ("internal_conflict", internal_conflict_score),
            ("external_conflict", external_conflict_score),
            ("economic_indicators", economic_indicators_score)
        ]
        categories.sort(key=lambda x: x[1], reverse=True)
        
        primary_category = categories[0][0] if categories[0][1] > 0 else "uncategorized"
        secondary_category = categories[1][0] if len(categories) > 1 and categories[1][1] > 0 else None
        
        # Extract relevant sentences for each category
        internal_conflict_sentences = self._extract_relevant_sentences(text, self.internal_conflict_patterns)
        external_conflict_sentences = self._extract_relevant_sentences(text, self.external_conflict_patterns)
        economic_indicators_sentences = self._extract_relevant_sentences(text, self.economic_indicators_patterns)
        
        return {
            "primary_category": primary_category,
            "secondary_category": secondary_category,
            "scores": {
                "internal_conflict": internal_conflict_score,
                "external_conflict": external_conflict_score,
                "economic_indicators": economic_indicators_score
            },
            "match_counts": {
                "internal_conflict": internal_conflict_count,
                "external_conflict": external_conflict_count,
                "economic_indicators": economic_indicators_count,
                "total": total_matches
            },
            "relevant_sentences": {
                "internal_conflict": internal_conflict_sentences,
                "external_conflict": external_conflict_sentences,
                "economic_indicators": economic_indicators_sentences
            }
        }
    
    def _count_matches(self, text: str, patterns: List[re.Pattern]) -> int:
        """
        Count matches for a set of patterns in text
        
        Args:
            text: Text to search in
            patterns: List of regex patterns
            
        Returns:
            Number of matches
        """
        count = 0
        for pattern in patterns:
            matches = pattern.findall(text)
            count += len(matches)
        return count
    
    def _extract_relevant_sentences(self, text: str, patterns: List[re.Pattern]) -> List[str]:
        """
        Extract sentences containing matches for patterns
        
        Args:
            text: Text to search in
            patterns: List of regex patterns
            
        Returns:
            List of relevant sentences
        """
        sentences = sent_tokenize(text)
        relevant_sentences = []
        
        for sentence in sentences:
            for pattern in patterns:
                if pattern.search(sentence.lower()):
                    relevant_sentences.append(sentence)
                    break  # Break after finding a match to avoid duplicates
        
        return relevant_sentences
    
    def calculate_priority_score(self, 
                               article: Dict[str, Any], 
                               classification: Dict[str, Any]) -> float:
        """
        Calculate priority score for an article based on classification and metadata
        
        Args:
            article: Article data
            classification: Classification results
            
        Returns:
            Priority score (0-100)
        """
        # Base score from classification confidence
        base_score = max(
            classification["scores"]["internal_conflict"],
            classification["scores"]["external_conflict"],
            classification["scores"]["economic_indicators"]
        )
        
        # Source credibility weight (0.3)
        source_credibility = self._calculate_source_credibility(article.get("source", "Unknown"))
        
        # Recency weight (0.25)
        recency = self._calculate_recency(article.get("published_date", ""))
        
        # Relevance to Dalio's framework (0.3)
        relevance = classification["match_counts"]["total"] / 10  # Normalize to 0-10 range
        relevance = min(relevance, 10)  # Cap at 10
        relevance = relevance / 10 * 100  # Convert to percentage
        
        # Geographic importance (0.15)
        geographic_importance = self._calculate_geographic_importance(article.get("content", ""))
        
        # Calculate weighted score
        weighted_score = (
            (source_credibility * 0.3) +
            (recency * 0.25) +
            (relevance * 0.3) +
            (geographic_importance * 0.15)
        )
        
        return weighted_score
    
    def _calculate_source_credibility(self, source: str) -> float:
        """
        Calculate source credibility score
        
        Args:
            source: Source name
            
        Returns:
            Credibility score (0-100)
        """
        # Define credibility scores for known sources
        credibility_scores = {
            "The Wall Street Journal": 90,
            "Financial Times": 90,
            "Bloomberg": 85,
            "Reuters": 85,
            "The Economist": 85,
            "CNBC": 75,
            "The New York Times": 80,
            "BBC": 80,
            "Twitter": 50,  # Lower credibility for social media
            "Unknown": 40
        }
        
        # Return credibility score for source, or default score for unknown sources
        for known_source, score in credibility_scores.items():
            if known_source.lower() in source.lower():
                return score
        
        return credibility_scores["Unknown"]
    
    def _calculate_recency(self, date_str: str) -> float:
        """
        Calculate recency score based on publication date
        
        Args:
            date_str: Publication date string
            
        Returns:
            Recency score (0-100)
        """
        if not date_str:
            return 50  # Default score for unknown dates
        
        try:
            # Parse date string
            if 'T' in date_str:
                # ISO format
                pub_date = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                # Try common formats
                for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']:
                    try:
                        pub_date = datetime.datetime.strptime(date_str, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return 50  # Default score if parsing fails
            
            # Calculate days since publication
            now = datetime.datetime.now()
            delta = now - pub_date
            days = delta.days
            
            # Calculate recency score
            if days <= 1:
                return 100  # Today or yesterday
            elif days <= 3:
                return 90  # Last 3 days
            elif days <= 7:
                return 80  # Last week
            elif days <= 14:
                return 70  # Last 2 weeks
            elif days <= 30:
                return 60  # Last month
            elif days <= 90:
                return 40  # Last 3 months
            elif days <= 180:
                return 30  # Last 6 months
            elif days <= 365:
                return 20  # Last year
            else:
                return 10  # Older than a year
        
        except Exception as e:
            logger.error(f"Error calculating recency: {e}")
            return 50  # Default score if calculation fails
    
    def _calculate_geographic_importance(self, content: str) -> float:
        """
        Calculate geographic importance score
        
        Args:
            content: Article content
            
        Returns:
            Geographic importance score (0-100)
        """
        # Define important regions and countries
        important_regions = {
            "global": 100,
            "worldwide": 100,
            "international": 90,
            "united states": 90,
            "us": 90,
            "china": 90,
            "europe": 85,
            "european union": 85,
            "eu": 85,
            "russia": 80,
            "japan": 80,
            "india": 80,
            "uk": 75,
            "united kingdom": 75,
            "germany": 75,
            "france": 75,
            "brazil": 70,
            "canada": 70,
            "australia": 70,
            "middle east": 75,
            "asia": 75,
            "latin america": 70,
            "africa": 70
        }
        
        # Check for mentions of important regions
        max_score = 0
        content_lower = content.lower()
        
        for region, score in important_regions.items():
            if re.search(r'\b' + re.escape(region) + r'\b', content_lower):
                max_score = max(max_score, score)
        
        return max_score if max_score > 0 else 50  # Default score if no regions mentioned


class ArticleClassifier:
    """
    Main class to classify articles using Ray Dalio's framework
    """
    def __init__(self):
        self.classifier = DalioFrameworkClassifier()
        self.output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def classify_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify a single article
        
        Args:
            article: Article data
            
        Returns:
            Article with classification data
        """
        # Extract text for classification
        text = article.get("title", "") + " " + article.get("content", "")
        
        # Classify text
        classification = self.classifier.classify_text(text)
        
        # Calculate priority score
        priority_score = self.classifier.calculate_priority_score(article, classification)
        
        # Add classification data to article
        classified_article = article.copy()
        classified_article["classification"] = classification
        classified_article["priority_score"] = priority_score
        
        return classified_article
    
    def classify_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Classify multiple articles
        
        Args:
            articles: List of articles
            
        Returns:
            List of articles with classification data
        """
        classified_articles = []
        
        for article in articles:
            classified_article = self.classify_article(article)
            classified_articles.append(classified_article)
        
        # Sort by priority score
        classified_articles.sort(key=lambda x: x.get("priority_score", 0), reverse=True)
        
        return classified_articles
    
    def classify_from_file(self, input_file: str) -> List[Dict[str, Any]]:
        """
        Classify articles from a JSON file
        
        Args:
            input_file: Path to input JSON file
            
        Returns:
            List of classified articles
        """
        try:
            with open(input_file, 'r') as f:
                articles = json.load(f)
            
            classified_articles = self.classify_articles(articles)
            
            # Save classified articles
            output_file = os.path.join(self.output_dir, f"classified_{os.path.basename(input_file)}")
            with open(output_file, 'w') as f:
                json.dump(classified_articles, f, indent=2)
            
            logger.info(f"Classified {len(classified_articles)} articles and saved to {output_file}")
            
            return classified_articles
        
        except Exception as e:
            logger.error(f"Error classifying articles from file: {e}")
            return []
    
    def generate_classification_summary(self, classified_articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate summary of classification results
        
        Args:
            classified_articles: List of classified articles
            
        Returns:
            Summary statistics
        """
        total_articles = len(classified_articles)
        
        # Count articles by primary category
        category_counts = {
            "internal_conflict": 0,
            "external_conflict": 0,
            "economic_indicators": 0,
            "uncategorized": 0
        }
        
        # Calculate average scores
        total_scores = {
            "internal_conflict": 0,
            "external_conflict": 0,
            "economic_indicators": 0
        }
        
        # Track high priority articles
        high_priority_articles = []
        
        for article in classified_articles:
            # Count by primary category
            primary_category = article.get("classification", {}).get("primary_category", "uncategorized")
            category_counts[primary_category] = category_counts.get(primary_category, 0) + 1
            
            # Sum scores for average calculation
            scores = article.get("classification", {}).get("scores", {})
            for category, score in scores.items():
                total_scores[category] = total_scores.get(category, 0) + score
            
            # Track high priority articles (score > 70)
            if article.get("priority_score", 0) > 70:
                high_priority_articles.append({
                    "title": article.get("title", ""),
                    "source": article.get("source", ""),
                    "primary_category": primary_category,
                    "priority_score": article.get("priority_score", 0)
                })
        
        # Calculate average scores
        avg_scores = {}
        for category, total in total_scores.items():
            avg_scores[category] = total / total_articles if total_articles > 0 else 0
        
        return {
            "total_articles": total_articles,
            "category_counts": category_counts,
            "average_scores": avg_scores,
            "high_priority_articles": high_priority_articles,
            "timestamp": datetime.datetime.now().isoformat()
        }


# Example usage
if __name__ == "__main__":
    # Create article classifier
    classifier = ArticleClassifier()
    
    # Example article
    example_article = {
        "title": "Global Trade Tensions Escalate as US and China Impose New Tariffs",
        "content": "Trade tensions between the United States and China escalated today as both countries announced new tariffs on each other's goods. The move comes amid growing concerns about the global economic outlook and rising geopolitical tensions. Analysts warn that this external conflict could lead to a prolonged trade war, affecting global supply chains and economic growth. Meanwhile, domestic political pressures in both countries make it difficult for leaders to back down, highlighting the complex interplay between internal and external conflicts in today's interconnected world.",
        "source": "Financial Times",
        "published_date": "2023-06-15T10:30:00Z",
        "url": "https://example.com/article1"
    }
    
    # Classify example article
    classified_article = classifier.classify_article(example_article)
    
    # Print classification results
    print(f"Title: {classified_article['title']}")
    print(f"Primary Category: {classified_article['classification']['primary_category']}")
    print(f"Secondary Category: {classified_article['classification']['secondary_category']}")
    print(f"Priority Score: {classified_article['priority_score']:.2f}")
    print("Category Scores:")
    for category, score in classified_article['classification']['scores'].items():
        print(f"  {category}: {score:.2f}")
