import os
import json
import logging
from typing import Dict, List, Any, Optional
from chatgpt_analyzer import ChatGPTIntegration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NewsAnalysisManager:
    """
    Manager for integrating ChatGPT analysis into the news processing pipeline
    """
    def __init__(self, db_manager=None, api_key: Optional[str] = None):
        # Import here to avoid circular imports
        if db_manager is None:
            import sys
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
            from database_manager import DatabaseManager
            self.db_manager = DatabaseManager()
        else:
            self.db_manager = db_manager
        
        # Initialize ChatGPT integration
        self.chatgpt = ChatGPTIntegration(api_key)
        
        # Create output directory
        self.output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def analyze_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze a batch of articles using ChatGPT
        
        Args:
            articles: List of articles to analyze
            
        Returns:
            List of analyzed articles
        """
        analyzed_articles = []
        
        for article in articles:
            try:
                logger.info(f"Analyzing article: {article.get('title', 'Untitled')}")
                
                # Skip articles that have already been analyzed
                if "analysis" in article:
                    logger.info("Article already analyzed, skipping")
                    analyzed_articles.append(article)
                    continue
                
                # Analyze article
                analyzed_article = self.chatgpt.analyze_article(article)
                
                # Store analysis in database
                if "error" not in analyzed_article:
                    # Update article with analysis
                    article_id = article.get("id")
                    if article_id:
                        # In a real implementation, we would update the article in the database
                        # For now, we'll just log it
                        logger.info(f"Would update article {article_id} with analysis in database")
                
                analyzed_articles.append(analyzed_article)
            
            except Exception as e:
                logger.error(f"Error analyzing article: {e}")
                # Add the original article with an error flag
                article["analysis_error"] = str(e)
                analyzed_articles.append(article)
        
        return analyzed_articles
    
    def generate_daily_report(self, date: str = None) -> Dict[str, Any]:
        """
        Generate a daily report using ChatGPT
        
        Args:
            date: Optional date for the report (default: today)
            
        Returns:
            Report data
        """
        try:
            # In a real implementation, we would fetch articles from the database for the specified date
            # For now, we'll use a mock approach
            
            # Get articles for each category
            internal_conflict_articles = self._get_mock_articles("internal_conflict")
            external_conflict_articles = self._get_mock_articles("external_conflict")
            economic_indicators_articles = self._get_mock_articles("economic_indicators")
            
            # Generate summaries for each category
            logger.info("Generating summary for internal conflict articles")
            internal_conflict_summary = self.chatgpt.generate_daily_summary(
                internal_conflict_articles, "internal_conflict"
            )
            
            logger.info("Generating summary for external conflict articles")
            external_conflict_summary = self.chatgpt.generate_daily_summary(
                external_conflict_articles, "external_conflict"
            )
            
            logger.info("Generating summary for economic indicators articles")
            economic_indicators_summary = self.chatgpt.generate_daily_summary(
                economic_indicators_articles, "economic_indicators"
            )
            
            # Generate overall summary
            logger.info("Generating overall summary")
            all_articles = internal_conflict_articles + external_conflict_articles + economic_indicators_articles
            overall_summary = self.chatgpt.generate_daily_summary(all_articles)
            
            # Analyze trends
            logger.info("Analyzing trends")
            trend_data = {
                "internal_conflict": self._get_mock_trend_data("internal_conflict"),
                "external_conflict": self._get_mock_trend_data("external_conflict"),
                "economic_indicators": self._get_mock_trend_data("economic_indicators")
            }
            trend_analysis = self.chatgpt.analyze_trends(trend_data)
            
            # Compile report
            report = {
                "date": date,
                "overall_summary": overall_summary,
                "category_summaries": {
                    "internal_conflict": internal_conflict_summary,
                    "external_conflict": external_conflict_summary,
                    "economic_indicators": economic_indicators_summary
                },
                "trend_analysis": trend_analysis
            }
            
            # Save report
            report_file = os.path.join(self.output_dir, f"daily_report_{date or 'today'}.json")
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Daily report saved to {report_file}")
            
            return report
        
        except Exception as e:
            logger.error(f"Error generating daily report: {e}")
            return {"error": str(e)}
    
    def analyze_specific_topic(self, topic: str, articles: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze a specific topic using ChatGPT
        
        Args:
            topic: Topic to analyze
            articles: Optional list of articles (if not provided, will fetch from database)
            
        Returns:
            Analysis results
        """
        try:
            # If articles not provided, fetch from database (mock for now)
            if articles is None:
                articles = self._get_mock_articles_for_topic(topic)
            
            if not articles:
                return {"error": "No articles found for topic"}
            
            # Create a special prompt for topic analysis
            prompt = [
                {"role": "system", "content": f"""
                You are an expert analyst working with Ray Dalio's "New World Order" framework.
                Your task is to analyze news articles related to the topic: {topic}.
                
                Based on the articles provided, generate:
                1. A comprehensive analysis of the topic from Ray Dalio's perspective
                2. Key implications for internal conflict, external conflict, and economic indicators
                3. Potential future developments
                4. Strategic recommendations
                
                Format your response as JSON with the following structure:
                {{
                    "topic_analysis": "Comprehensive analysis here",
                    "implications": {{
                        "internal_conflict": "Implications here",
                        "external_conflict": "Implications here",
                        "economic_indicators": "Implications here"
                    }},
                    "future_developments": ["Development1", "Development2"],
                    "strategic_recommendations": ["Recommendation1", "Recommendation2"],
                    "ray_dalio_perspective": "How Ray Dalio might interpret this topic"
                }}
                """
                },
                {"role": "user", "content": "Articles to analyze:\n\n" + "\n\n".join([
                    f"Title: {article.get('title', '')}\nContent: {article.get('content', '')}"
                    for article in articles[:5]  # Limit to 5 articles to avoid token limits
                ])}
            ]
            
            # Call ChatGPT API
            response = self.chatgpt._call_chatgpt_api(prompt)
            
            # Parse response
            analysis = self.chatgpt._parse_analysis_response(response)
            
            # Save analysis
            analysis_file = os.path.join(self.output_dir, f"topic_analysis_{topic.replace(' ', '_')}.json")
            with open(analysis_file, 'w') as f:
                json.dump(analysis, f, indent=2)
            
            logger.info(f"Topic analysis saved to {analysis_file}")
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error analyzing topic: {e}")
            return {"error": str(e)}
    
    def _get_mock_articles(self, category: str) -> List[Dict[str, Any]]:
        """
        Get mock articles for a category
        
        Args:
            category: Category to get articles for
            
        Returns:
            List of articles
        """
        # Mock articles for each category
        mock_articles = {
            "internal_conflict": [
                {
                    "title": "Protests Erupt in Major Cities Over Economic Inequality",
                    "content": "Thousands took to the streets in several major cities today, protesting growing economic inequality and government policies.",
                    "source": "The New York Times",
                    "published_date": "2023-06-14T14:45:00Z",
                    "classification": {"primary_category": "internal_conflict"}
                },
                {
                    "title": "Political Polarization Reaches New Heights in Legislative Bodies",
                    "content": "Political analysts report unprecedented levels of polarization in legislative bodies, hampering governance and policy implementation.",
                    "source": "The Washington Post",
                    "published_date": "2023-06-11T11:10:00Z",
                    "classification": {"primary_category": "internal_conflict"}
                }
            ],
            "external_conflict": [
                {
                    "title": "Global Trade Tensions Escalate as US and China Impose New Tariffs",
                    "content": "Trade tensions between the United States and China escalated today as both countries announced new tariffs on each other's goods.",
                    "source": "Financial Times",
                    "published_date": "2023-06-15T10:30:00Z",
                    "classification": {"primary_category": "external_conflict"}
                },
                {
                    "title": "Diplomatic Relations Deteriorate Between European Nations Over Resource Disputes",
                    "content": "Diplomatic tensions are rising between several European nations as disputes over shared resources intensify.",
                    "source": "Reuters",
                    "published_date": "2023-06-12T16:20:00Z",
                    "classification": {"primary_category": "external_conflict"}
                }
            ],
            "economic_indicators": [
                {
                    "title": "Central Banks Signal Shift in Monetary Policy Amid Inflation Concerns",
                    "content": "Several central banks have signaled a potential shift in monetary policy as inflation concerns grow in major economies.",
                    "source": "Bloomberg",
                    "published_date": "2023-06-13T09:15:00Z",
                    "classification": {"primary_category": "economic_indicators"}
                },
                {
                    "title": "Global Debt Levels Reach Record High, Raising Stability Concerns",
                    "content": "Global debt has reached a record high, raising concerns about long-term financial stability and economic growth prospects.",
                    "source": "The Economist",
                    "published_date": "2023-06-10T08:45:00Z",
                    "classification": {"primary_category": "economic_indicators"}
                }
            ]
        }
        
        return mock_articles.get(category, [])
    
    def _get_mock_trend_data(self, category: str) -> List[Dict[str, Any]]:
        """
        Get mock trend data for a category
        
        Args:
            category: Category to get trend data for
            
        Returns:
            List of trend data points
        """
        # Mock trend data
        dates = [
            "2023-05-15", "2023-05-22", "2023-05-29",
            "2023-06-05", "2023-06-12", "2023-06-15"
        ]
        
        if category == "internal_conflict":
            values = [15, 18, 22, 25, 28, 30]
        elif category == "external_conflict":
            values = [20, 22, 25, 28, 30, 32]
        else:  # economic_indicators
            values = [25, 28, 30, 32, 35, 38]
        
        return [{"date": date, "value": value} for date, value in zip(dates, values)]
    
    def _get_mock_articles_for_topic(self, topic: str) -> List[Dict[str, Any]]:
        """
        Get mock articles for a specific topic
        
        Args:
            topic: Topic to get articles for
            
        Returns:
            List of articles
        """
        # Mock articles for specific topics
        mock_topic_articles = {
            "inflation": [
                {
                    "title": "Inflation Reaches 40-Year High in Major Economies",
                    "content": "Inflation has reached a 40-year high in several major economies, putting pressure on central banks to raise interest rates.",
                    "source": "Financial Times",
                    "published_date": "2023-06-15T10:30:00Z"
                },
                {
                    "title": "Central Banks Signal Aggressive Rate Hikes to Combat Inflation",
                    "content": "Central banks around the world are signaling more aggressive interest rate hikes to combat persistent inflation pressures.",
                    "source": "Bloomberg",
                    "published_date": "2023-06-13T09:15:00Z"
                }
            ],
            "geopolitical tension": [
                {
                    "title": "Rising Tensions in South China Sea as Naval Presence Increases",
                    "content": "Geopolitical tensions are rising in the South China Sea as multiple nations increase their naval presence in disputed waters.",
                    "source": "Reuters",
                    "published_date": "2023-06-14T14:45:00Z"
                },
                {
                    "title": "Diplomatic Crisis Deepens Between Major Powers Over Security Concerns",
                    "content": "A diplomatic crisis is deepening between major global powers as security concerns and territorial disputes remain unresolved.",
                    "source": "The New York Times",
                    "published_date": "2023-06-12T16:20:00Z"
                }
            ],
            "debt crisis": [
                {
                    "title": "Emerging Markets Face Debt Crisis as Interest Rates Rise",
                    "content": "Several emerging market economies are facing a potential debt crisis as global interest rates rise and currency values decline.",
                    "source": "The Economist",
                    "published_date": "2023-06-11T11:10:00Z"
                },
                {
                    "title": "Global Debt Levels Reach Record High, Raising Stability Concerns",
                    "content": "Global debt has reached a record high, raising concerns about long-term financial stability and economic growth prospects.",
                    "source": "The Economist",
                    "published_date": "2023-06-10T08:45:00Z"
                }
            ]
        }
        
        # Try to match the topic to one of our mock topics
        for mock_topic, articles in mock_topic_articles.items():
            if topic.lower() in mock_topic.lower():
                return articles
        
        # If no match, return empty list
        return []


# Example usage
if __name__ == "__main__":
    # Create news analysis manager
    analysis_manager = NewsAnalysisManager()
    
    # Example article
    example_article = {
        "title": "Global Trade Tensions Escalate as US and China Impose New Tariffs",
        "content": "Trade tensions between the United States and China escalated today as both countries announced new tariffs on each other's goods. The move comes amid growing concerns about the global economic outlook and rising geopolitical tensions."
    }
    
    # Analyze article
    analyzed_articles = analysis_manager.analyze_articles([example_article])
    
    print(json.dumps(analyzed_articles, indent=2))
    
    # Generate daily report
    report = analysis_manager.generate_daily_report("2023-06-15")
    
    print(json.dumps(report, indent=2))
