import os
import json
import logging
import requests
from typing import Dict, List, Any, Optional
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ChatGPTIntegration:
    """
    Integration with ChatGPT for news analysis and summarization
    """
    def __init__(self, api_key: Optional[str] = None):
        # Use provided API key or get from environment variable
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("No OpenAI API key provided. ChatGPT integration will not function.")
        
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-4"  # Using GPT-4 for best analysis capabilities
    
    def analyze_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a news article using ChatGPT
        
        Args:
            article: Article data including title and content
            
        Returns:
            Analysis results
        """
        if not self.api_key:
            return {"error": "No API key provided"}
        
        try:
            # Extract article text
            title = article.get("title", "")
            content = article.get("content", "")
            
            if not content:
                return {"error": "No article content provided"}
            
            # Create prompt for ChatGPT
            prompt = self._create_analysis_prompt(title, content)
            
            # Call ChatGPT API
            response = self._call_chatgpt_api(prompt)
            
            # Parse response
            analysis = self._parse_analysis_response(response)
            
            # Add analysis to article
            article_with_analysis = {**article, "analysis": analysis}
            
            return article_with_analysis
        
        except Exception as e:
            logger.error(f"Error analyzing article: {e}")
            return {"error": str(e)}
    
    def generate_daily_summary(self, articles: List[Dict[str, Any]], category: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a daily summary of news articles using ChatGPT
        
        Args:
            articles: List of articles to summarize
            category: Optional category to filter articles
            
        Returns:
            Summary data
        """
        if not self.api_key:
            return {"error": "No API key provided"}
        
        try:
            # Filter articles by category if provided
            if category:
                filtered_articles = [
                    article for article in articles 
                    if article.get("classification", {}).get("primary_category") == category
                ]
            else:
                filtered_articles = articles
            
            if not filtered_articles:
                return {"error": "No articles to summarize"}
            
            # Extract article titles and summaries
            article_texts = []
            for article in filtered_articles[:10]:  # Limit to 10 articles to avoid token limits
                title = article.get("title", "")
                summary = article.get("summary", "")
                article_texts.append(f"Title: {title}\nSummary: {summary}")
            
            # Create prompt for ChatGPT
            prompt = self._create_summary_prompt(article_texts, category)
            
            # Call ChatGPT API
            response = self._call_chatgpt_api(prompt)
            
            # Parse response
            summary = self._parse_summary_response(response)
            
            return summary
        
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return {"error": str(e)}
    
    def analyze_trends(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze trends in news data using ChatGPT
        
        Args:
            data: Trend data including time series and categories
            
        Returns:
            Trend analysis
        """
        if not self.api_key:
            return {"error": "No API key provided"}
        
        try:
            # Extract trend data
            internal_conflict = data.get("internal_conflict", [])
            external_conflict = data.get("external_conflict", [])
            economic_indicators = data.get("economic_indicators", [])
            
            # Create prompt for ChatGPT
            prompt = self._create_trend_analysis_prompt(internal_conflict, external_conflict, economic_indicators)
            
            # Call ChatGPT API
            response = self._call_chatgpt_api(prompt)
            
            # Parse response
            analysis = self._parse_trend_analysis_response(response)
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            return {"error": str(e)}
    
    def _create_analysis_prompt(self, title: str, content: str) -> List[Dict[str, str]]:
        """
        Create a prompt for article analysis
        
        Args:
            title: Article title
            content: Article content
            
        Returns:
            Formatted prompt for ChatGPT
        """
        return [
            {"role": "system", "content": """
            You are an expert analyst working with Ray Dalio's "New World Order" framework. 
            Your task is to analyze news articles and classify them according to Ray Dalio's concepts of internal conflict, 
            external conflict, and economic indicators. 
            
            For each article, provide:
            1. A concise summary (2-3 sentences)
            2. Classification as primarily internal conflict, external conflict, or economic indicators
            3. Key entities mentioned (people, organizations, countries)
            4. Potential implications based on Ray Dalio's framework
            5. A priority score from 0-100 indicating how significant this news is within the framework
            
            Format your response as JSON with the following structure:
            {
                "summary": "Concise summary here",
                "classification": {
                    "primary_category": "internal_conflict|external_conflict|economic_indicators",
                    "confidence": 85
                },
                "entities": ["Entity1", "Entity2"],
                "implications": "Analysis of implications here",
                "priority_score": 75,
                "ray_dalio_perspective": "How Ray Dalio might interpret this news"
            }
            """
            },
            {"role": "user", "content": f"Title: {title}\n\nContent: {content}"}
        ]
    
    def _create_summary_prompt(self, article_texts: List[str], category: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Create a prompt for daily summary generation
        
        Args:
            article_texts: List of article texts
            category: Optional category for filtering
            
        Returns:
            Formatted prompt for ChatGPT
        """
        category_text = f" in the category of {category.replace('_', ' ')}" if category else ""
        
        return [
            {"role": "system", "content": f"""
            You are an expert analyst working with Ray Dalio's "New World Order" framework.
            Your task is to generate a comprehensive daily summary of news articles{category_text}.
            
            Analyze the following articles and provide:
            1. A concise executive summary (3-5 sentences)
            2. Key themes and patterns across the articles
            3. Potential implications based on Ray Dalio's framework
            4. Areas to monitor in the coming days
            
            Format your response as JSON with the following structure:
            {{
                "executive_summary": "Summary here",
                "key_themes": ["Theme1", "Theme2", "Theme3"],
                "implications": "Analysis of implications here",
                "areas_to_monitor": ["Area1", "Area2"],
                "ray_dalio_perspective": "How Ray Dalio might interpret these developments"
            }}
            """
            },
            {"role": "user", "content": "Articles to summarize:\n\n" + "\n\n".join(article_texts)}
        ]
    
    def _create_trend_analysis_prompt(self, internal_conflict: List[Any], external_conflict: List[Any], economic_indicators: List[Any]) -> List[Dict[str, str]]:
        """
        Create a prompt for trend analysis
        
        Args:
            internal_conflict: Internal conflict trend data
            external_conflict: External conflict trend data
            economic_indicators: Economic indicators trend data
            
        Returns:
            Formatted prompt for ChatGPT
        """
        return [
            {"role": "system", "content": """
            You are an expert analyst working with Ray Dalio's "New World Order" framework.
            Your task is to analyze trends in news data across internal conflict, external conflict, and economic indicators.
            
            Based on the trend data provided, generate:
            1. An analysis of the overall trajectory for each category
            2. Correlations between different categories
            3. Potential future developments based on Ray Dalio's framework
            4. Strategic recommendations for decision-makers
            
            Format your response as JSON with the following structure:
            {
                "trajectory_analysis": {
                    "internal_conflict": "Analysis here",
                    "external_conflict": "Analysis here",
                    "economic_indicators": "Analysis here"
                },
                "correlations": ["Correlation1", "Correlation2"],
                "future_developments": "Analysis of potential developments",
                "strategic_recommendations": ["Recommendation1", "Recommendation2"],
                "ray_dalio_perspective": "How Ray Dalio might interpret these trends"
            }
            """
            },
            {"role": "user", "content": f"""
            Trend data to analyze:
            
            Internal Conflict Trends:
            {json.dumps(internal_conflict)}
            
            External Conflict Trends:
            {json.dumps(external_conflict)}
            
            Economic Indicator Trends:
            {json.dumps(economic_indicators)}
            """
            }
        ]
    
    def _call_chatgpt_api(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Call the ChatGPT API
        
        Args:
            messages: List of message objects for the conversation
            
        Returns:
            API response
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.3,  # Lower temperature for more consistent, analytical responses
            "max_tokens": 1000
        }
        
        # Implement retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=data
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:  # Rate limit error
                    wait_time = (2 ** attempt) + 1  # Exponential backoff
                    logger.warning(f"Rate limit reached. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"API error: {response.status_code} - {response.text}")
                    break
            
            except Exception as e:
                logger.error(f"Error calling ChatGPT API: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    break
        
        return {"error": "Failed to get response from ChatGPT API"}
    
    def _parse_analysis_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse the response from ChatGPT for article analysis
        
        Args:
            response: API response
            
        Returns:
            Parsed analysis
        """
        try:
            if "error" in response:
                return {"error": response["error"]}
            
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # Extract JSON from content
            try:
                # Find JSON in the response
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_str = content[json_start:json_end]
                    analysis = json.loads(json_str)
                    return analysis
                else:
                    # If no JSON found, try to parse the whole content
                    return json.loads(content)
            
            except json.JSONDecodeError:
                # If JSON parsing fails, return a structured version of the text
                return {
                    "summary": content.split("\n\n")[0] if "\n\n" in content else content[:200],
                    "raw_analysis": content
                }
        
        except Exception as e:
            logger.error(f"Error parsing analysis response: {e}")
            return {"error": str(e)}
    
    def _parse_summary_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse the response from ChatGPT for daily summary
        
        Args:
            response: API response
            
        Returns:
            Parsed summary
        """
        # Similar to _parse_analysis_response
        return self._parse_analysis_response(response)
    
    def _parse_trend_analysis_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse the response from ChatGPT for trend analysis
        
        Args:
            response: API response
            
        Returns:
            Parsed trend analysis
        """
        # Similar to _parse_analysis_response
        return self._parse_analysis_response(response)


# Example usage
if __name__ == "__main__":
    # Create ChatGPT integration
    chatgpt = ChatGPTIntegration()
    
    # Example article
    example_article = {
        "title": "Global Trade Tensions Escalate as US and China Impose New Tariffs",
        "content": "Trade tensions between the United States and China escalated today as both countries announced new tariffs on each other's goods. The move comes amid growing concerns about the global economic outlook and rising geopolitical tensions."
    }
    
    # Analyze article
    analyzed_article = chatgpt.analyze_article(example_article)
    
    print(json.dumps(analyzed_article, indent=2))
