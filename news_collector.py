import requests
import feedparser
import json
import os
import datetime
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NewsAPIAdapter:
    """
    Adapter for the NewsAPI service
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
        self.headers = {
            "X-Api-Key": self.api_key
        }
    
    def get_top_headlines(self, 
                         country: str = "us", 
                         category: Optional[str] = None,
                         query: Optional[str] = None,
                         page_size: int = 100) -> Dict[str, Any]:
        """
        Get top headlines from NewsAPI
        
        Args:
            country: 2-letter ISO 3166-1 country code
            category: Category of news (business, entertainment, general, health, science, sports, technology)
            query: Keywords or phrases to search for
            page_size: Number of results to return per page (max 100)
            
        Returns:
            JSON response from the API
        """
        endpoint = f"{self.base_url}/top-headlines"
        params = {
            "country": country,
            "pageSize": page_size
        }
        
        if category:
            params["category"] = category
            
        if query:
            params["q"] = query
            
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching top headlines: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_everything(self, 
                      query: str,
                      from_date: Optional[str] = None,
                      to_date: Optional[str] = None,
                      language: str = "en",
                      sort_by: str = "publishedAt",
                      page_size: int = 100) -> Dict[str, Any]:
        """
        Search for news articles from NewsAPI
        
        Args:
            query: Keywords or phrases to search for
            from_date: A date in ISO 8601 format (e.g. 2023-12-25)
            to_date: A date in ISO 8601 format (e.g. 2023-12-25)
            language: 2-letter ISO-639-1 language code
            sort_by: The order to sort articles (relevancy, popularity, publishedAt)
            page_size: Number of results to return per page (max 100)
            
        Returns:
            JSON response from the API
        """
        endpoint = f"{self.base_url}/everything"
        params = {
            "q": query,
            "language": language,
            "sortBy": sort_by,
            "pageSize": page_size
        }
        
        if from_date:
            params["from"] = from_date
            
        if to_date:
            params["to"] = to_date
            
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching articles: {e}")
            return {"status": "error", "message": str(e)}


class RSSFeedAdapter:
    """
    Adapter for RSS feeds
    """
    def __init__(self):
        self.feeds = {
            "wsj_economy": "https://feeds.a.dj.com/rss/RSSEconomy.xml",
            "wsj_world": "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
            "ft_world": "https://www.ft.com/world?format=rss",
            "economist": "https://www.economist.com/finance-and-economics/rss.xml",
            "bloomberg": "https://feeds.bloomberg.com/markets/news.rss"
        }
    
    def get_feed(self, feed_name: str) -> Dict[str, Any]:
        """
        Get articles from an RSS feed
        
        Args:
            feed_name: Name of the feed to fetch
            
        Returns:
            Parsed feed data
        """
        if feed_name not in self.feeds:
            logger.error(f"Feed {feed_name} not found")
            return {"status": "error", "message": f"Feed {feed_name} not found"}
        
        try:
            feed = feedparser.parse(self.feeds[feed_name])
            return {
                "status": "ok",
                "feed": feed_name,
                "articles": [
                    {
                        "title": entry.title,
                        "description": entry.summary if hasattr(entry, 'summary') else "",
                        "url": entry.link,
                        "publishedAt": entry.published if hasattr(entry, 'published') else "",
                        "source": {
                            "name": feed.feed.title if hasattr(feed.feed, 'title') else feed_name
                        }
                    }
                    for entry in feed.entries
                ]
            }
        except Exception as e:
            logger.error(f"Error fetching RSS feed {feed_name}: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_all_feeds(self) -> Dict[str, Any]:
        """
        Get articles from all configured RSS feeds
        
        Returns:
            Combined feed data
        """
        all_articles = []
        for feed_name in self.feeds:
            feed_data = self.get_feed(feed_name)
            if feed_data["status"] == "ok":
                all_articles.extend(feed_data["articles"])
        
        return {
            "status": "ok",
            "totalResults": len(all_articles),
            "articles": all_articles
        }


class TwitterAdapter:
    """
    Adapter for Twitter API to fetch analyst commentary
    Note: This is a mock implementation as actual Twitter API requires authentication
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.analysts = [
            "RayDalio",
            "MohamedEBElerian",
            "Nouriel",
            "LHSummers",
            "ProfJNSheffrin",
            "JeffDSachs"
        ]
    
    def get_analyst_tweets(self, username: str, count: int = 10) -> Dict[str, Any]:
        """
        Get tweets from a specific analyst
        
        Args:
            username: Twitter handle of the analyst
            count: Number of tweets to fetch
            
        Returns:
            Mock tweet data for demonstration
        """
        # In a real implementation, this would call the Twitter API
        # For now, we'll return mock data
        
        # Check if we have a mock data file for this analyst
        mock_file = os.path.join(os.path.dirname(__file__), "mock_data", f"{username.lower()}_tweets.json")
        
        if os.path.exists(mock_file):
            try:
                with open(mock_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading mock data for {username}: {e}")
        
        # Generate mock data if no file exists
        current_date = datetime.datetime.now()
        tweets = []
        
        for i in range(count):
            date = current_date - datetime.timedelta(days=i)
            tweets.append({
                "id": f"mock_{username}_{i}",
                "created_at": date.isoformat(),
                "text": f"Mock tweet {i+1} from {username} about economic trends and global markets. #economics #investing",
                "user": {
                    "screen_name": username,
                    "name": username.replace("_", " "),
                    "profile_image_url": "https://via.placeholder.com/48"
                }
            })
        
        return {
            "status": "ok",
            "username": username,
            "tweets": tweets
        }
    
    def get_all_analysts_tweets(self, count_per_analyst: int = 5) -> Dict[str, Any]:
        """
        Get tweets from all configured analysts
        
        Args:
            count_per_analyst: Number of tweets to fetch per analyst
            
        Returns:
            Combined tweet data
        """
        all_tweets = []
        for analyst in self.analysts:
            analyst_data = self.get_analyst_tweets(analyst, count_per_analyst)
            if analyst_data["status"] == "ok":
                for tweet in analyst_data["tweets"]:
                    tweet["analyst"] = analyst
                    all_tweets.append(tweet)
        
        return {
            "status": "ok",
            "totalResults": len(all_tweets),
            "tweets": all_tweets
        }


class DataParser:
    """
    Parser to standardize data from different sources
    """
    def parse_newsapi_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse an article from NewsAPI into standard format
        
        Args:
            article: Article data from NewsAPI
            
        Returns:
            Standardized article data
        """
        return {
            "title": article.get("title", ""),
            "content": article.get("description", "") + " " + article.get("content", ""),
            "summary": article.get("description", ""),
            "url": article.get("url", ""),
            "published_date": article.get("publishedAt", ""),
            "source": article.get("source", {}).get("name", "Unknown"),
            "author": article.get("author", ""),
            "image_url": article.get("urlToImage", ""),
            "raw_data": article,
            "data_source": "newsapi"
        }
    
    def parse_rss_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse an article from RSS feed into standard format
        
        Args:
            article: Article data from RSS feed
            
        Returns:
            Standardized article data
        """
        return {
            "title": article.get("title", ""),
            "content": article.get("description", ""),
            "summary": article.get("description", ""),
            "url": article.get("url", ""),
            "published_date": article.get("publishedAt", ""),
            "source": article.get("source", {}).get("name", "Unknown"),
            "author": "",
            "image_url": "",
            "raw_data": article,
            "data_source": "rss"
        }
    
    def parse_tweet(self, tweet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse a tweet into standard format
        
        Args:
            tweet: Tweet data
            
        Returns:
            Standardized tweet data
        """
        return {
            "title": f"Tweet from {tweet.get('user', {}).get('name', 'Unknown')}",
            "content": tweet.get("text", ""),
            "summary": tweet.get("text", ""),
            "url": f"https://twitter.com/{tweet.get('user', {}).get('screen_name', 'unknown')}/status/{tweet.get('id', '')}",
            "published_date": tweet.get("created_at", ""),
            "source": "Twitter",
            "author": tweet.get("user", {}).get("name", "Unknown"),
            "image_url": tweet.get("user", {}).get("profile_image_url", ""),
            "raw_data": tweet,
            "data_source": "twitter",
            "analyst": tweet.get("analyst", "")
        }
    
    def standardize_data(self, data: Dict[str, Any], data_type: str) -> List[Dict[str, Any]]:
        """
        Convert data from various sources into a standard format
        
        Args:
            data: Data from a source
            data_type: Type of data (newsapi, rss, twitter)
            
        Returns:
            List of standardized data items
        """
        if data_type == "newsapi":
            if data.get("status") != "ok":
                logger.error(f"Error in NewsAPI response: {data.get('message', 'Unknown error')}")
                return []
            
            return [self.parse_newsapi_article(article) for article in data.get("articles", [])]
        
        elif data_type == "rss":
            if data.get("status") != "ok":
                logger.error(f"Error in RSS feed: {data.get('message', 'Unknown error')}")
                return []
            
            return [self.parse_rss_article(article) for article in data.get("articles", [])]
        
        elif data_type == "twitter":
            if data.get("status") != "ok":
                logger.error(f"Error in Twitter data: {data.get('message', 'Unknown error')}")
                return []
            
            return [self.parse_tweet(tweet) for tweet in data.get("tweets", [])]
        
        else:
            logger.error(f"Unknown data type: {data_type}")
            return []


class DataCollector:
    """
    Main class to collect data from all sources
    """
    def __init__(self, newsapi_key: Optional[str] = None):
        self.newsapi = NewsAPIAdapter(api_key=newsapi_key or "mock_key")
        self.rss = RSSFeedAdapter()
        self.twitter = TwitterAdapter()
        self.parser = DataParser()
    
    def collect_news_articles(self, 
                             query: Optional[str] = None,
                             from_date: Optional[str] = None,
                             to_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Collect news articles from all sources
        
        Args:
            query: Keywords to search for
            from_date: Start date for search
            to_date: End date for search
            
        Returns:
            List of standardized articles
        """
        all_articles = []
        
        # Get articles from NewsAPI
        if query:
            newsapi_data = self.newsapi.get_everything(
                query=query,
                from_date=from_date,
                to_date=to_date
            )
        else:
            newsapi_data = self.newsapi.get_top_headlines(category="business")
        
        all_articles.extend(self.parser.standardize_data(newsapi_data, "newsapi"))
        
        # Get articles from RSS feeds
        rss_data = self.rss.get_all_feeds()
        all_articles.extend(self.parser.standardize_data(rss_data, "rss"))
        
        return all_articles
    
    def collect_analyst_commentary(self) -> List[Dict[str, Any]]:
        """
        Collect analyst commentary from Twitter
        
        Returns:
            List of standardized tweets
        """
        twitter_data = self.twitter.get_all_analysts_tweets()
        return self.parser.standardize_data(twitter_data, "twitter")
    
    def collect_all_data(self, 
                        query: Optional[str] = None,
                        from_date: Optional[str] = None,
                        to_date: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Collect all data from all sources
        
        Args:
            query: Keywords to search for
            from_date: Start date for search
            to_date: End date for search
            
        Returns:
            Dictionary with articles and analyst commentary
        """
        articles = self.collect_news_articles(query, from_date, to_date)
        commentary = self.collect_analyst_commentary()
        
        return {
            "articles": articles,
            "analyst_commentary": commentary
        }


# Example usage
if __name__ == "__main__":
    # Create data collector
    collector = DataCollector()
    
    # Collect data
    data = collector.collect_all_data(query="inflation OR recession OR \"interest rates\"")
    
    # Print summary
    print(f"Collected {len(data['articles'])} articles and {len(data['analyst_commentary'])} analyst comments")
    
    # Save to file for testing
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, "collected_data.json"), "w") as f:
        json.dump(data, f, indent=2)
