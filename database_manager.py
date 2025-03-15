import sqlite3
import os
import json
import logging
from typing import Dict, List, Any, Optional
import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Manager for SQLite database operations
    """
    def __init__(self, db_path: str = None):
        # Set default database path if not provided
        if db_path is None:
            db_dir = os.path.join(os.path.dirname(__file__), "data")
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, "ray_dalio_dashboard.db")
        
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self) -> None:
        """
        Connect to the SQLite database
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            self.cursor = self.conn.cursor()
            logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise
    
    def close(self) -> None:
        """
        Close the database connection
        """
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def create_tables(self) -> None:
        """
        Create database tables if they don't exist
        """
        try:
            self.connect()
            
            # Create Articles table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                summary TEXT,
                url TEXT,
                published_date TEXT,
                source TEXT,
                author TEXT,
                image_url TEXT,
                priority_score REAL,
                primary_category TEXT,
                secondary_category TEXT,
                created_at TEXT NOT NULL
            )
            ''')
            
            # Create Categories table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT
            )
            ''')
            
            # Create ArticleCategories table (many-to-many relationship)
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ArticleCategories (
                article_id INTEGER,
                category_id INTEGER,
                confidence_score REAL,
                PRIMARY KEY (article_id, category_id),
                FOREIGN KEY (article_id) REFERENCES Articles (id),
                FOREIGN KEY (category_id) REFERENCES Categories (id)
            )
            ''')
            
            # Create Analysts table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Analysts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                organization TEXT,
                expertise TEXT,
                credibility_score REAL
            )
            ''')
            
            # Create AnalystCommentary table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS AnalystCommentary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analyst_id INTEGER,
                content TEXT NOT NULL,
                date TEXT,
                source TEXT,
                url TEXT,
                priority_score REAL,
                primary_category TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (analyst_id) REFERENCES Analysts (id)
            )
            ''')
            
            # Create Metrics table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT
            )
            ''')
            
            # Create TimeSeries table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS TimeSeries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_id INTEGER,
                date TEXT NOT NULL,
                value REAL NOT NULL,
                FOREIGN KEY (metric_id) REFERENCES Metrics (id)
            )
            ''')
            
            # Create Keywords table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL UNIQUE,
                category TEXT
            )
            ''')
            
            # Create ArticleKeywords table (many-to-many relationship)
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ArticleKeywords (
                article_id INTEGER,
                keyword_id INTEGER,
                PRIMARY KEY (article_id, keyword_id),
                FOREIGN KEY (article_id) REFERENCES Articles (id),
                FOREIGN KEY (keyword_id) REFERENCES Keywords (id)
            )
            ''')
            
            # Create Reports table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                report_date TEXT NOT NULL,
                report_type TEXT,
                created_at TEXT NOT NULL
            )
            ''')
            
            # Insert default categories
            self.cursor.execute('''
            INSERT OR IGNORE INTO Categories (name, description)
            VALUES 
                ('internal_conflict', 'Civil unrest, domestic policy disputes, social tensions'),
                ('external_conflict', 'International tensions, trade disputes, military conflicts'),
                ('economic_indicators', 'Interest rates, inflation, GDP, unemployment')
            ''')
            
            # Insert default metrics
            self.cursor.execute('''
            INSERT OR IGNORE INTO Metrics (name, description)
            VALUES 
                ('internal_conflict_count', 'Daily count of internal conflict articles'),
                ('external_conflict_count', 'Daily count of external conflict articles'),
                ('economic_indicators_count', 'Daily count of economic indicators articles'),
                ('internal_conflict_score', 'Average priority score of internal conflict articles'),
                ('external_conflict_score', 'Average priority score of external conflict articles'),
                ('economic_indicators_score', 'Average priority score of economic indicators articles')
            ''')
            
            self.conn.commit()
            logger.info("Database tables created successfully")
        
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {e}")
            if self.conn:
                self.conn.rollback()
            raise
        
        finally:
            self.close()
    
    def insert_article(self, article: Dict[str, Any]) -> int:
        """
        Insert an article into the database
        
        Args:
            article: Article data
            
        Returns:
            ID of the inserted article
        """
        try:
            self.connect()
            
            # Extract classification data
            classification = article.get("classification", {})
            primary_category = classification.get("primary_category", "uncategorized")
            secondary_category = classification.get("secondary_category")
            priority_score = article.get("priority_score", 0)
            
            # Insert article
            self.cursor.execute('''
            INSERT INTO Articles (
                title, content, summary, url, published_date, source, author, 
                image_url, priority_score, primary_category, secondary_category, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                article.get("title", ""),
                article.get("content", ""),
                article.get("summary", ""),
                article.get("url", ""),
                article.get("published_date", ""),
                article.get("source", ""),
                article.get("author", ""),
                article.get("image_url", ""),
                priority_score,
                primary_category,
                secondary_category,
                datetime.datetime.now().isoformat()
            ))
            
            article_id = self.cursor.lastrowid
            
            # Insert article-category relationships
            for category, score in classification.get("scores", {}).items():
                if score > 0:
                    # Get category ID
                    self.cursor.execute("SELECT id FROM Categories WHERE name = ?", (category,))
                    result = self.cursor.fetchone()
                    if result:
                        category_id = result["id"]
                        
                        # Insert relationship
                        self.cursor.execute('''
                        INSERT INTO ArticleCategories (article_id, category_id, confidence_score)
                        VALUES (?, ?, ?)
                        ''', (article_id, category_id, score))
            
            # Extract and insert keywords
            if "content" in article:
                # This is a simplified approach - in a real implementation, 
                # we would use NLP to extract keywords
                words = article["content"].lower().split()
                unique_words = set(word for word in words if len(word) > 4)
                for word in list(unique_words)[:10]:  # Limit to 10 keywords
                    # Insert keyword if it doesn't exist
                    self.cursor.execute('''
                    INSERT OR IGNORE INTO Keywords (keyword, category)
                    VALUES (?, ?)
                    ''', (word, primary_category))
                    
                    # Get keyword ID
                    self.cursor.execute("SELECT id FROM Keywords WHERE keyword = ?", (word,))
                    result = self.cursor.fetchone()
                    if result:
                        keyword_id = result["id"]
                        
                        # Insert relationship
                        self.cursor.execute('''
                        INSERT OR IGNORE INTO ArticleKeywords (article_id, keyword_id)
                        VALUES (?, ?)
                        ''', (article_id, keyword_id))
            
            self.conn.commit()
            logger.info(f"Article inserted with ID: {article_id}")
            
            return article_id
        
        except sqlite3.Error as e:
            logger.error(f"Error inserting article: {e}")
            if self.conn:
                self.conn.rollback()
            raise
        
        finally:
            self.close()
    
    def insert_analyst_commentary(self, commentary: Dict[str, Any]) -> int:
        """
        Insert analyst commentary into the database
        
        Args:
            commentary: Commentary data
            
        Returns:
            ID of the inserted commentary
        """
        try:
            self.connect()
            
            # Check if analyst exists
            analyst_name = commentary.get("analyst_name", "")
            self.cursor.execute("SELECT id FROM Analysts WHERE name = ?", (analyst_name,))
            result = self.cursor.fetchone()
            
            if result:
                analyst_id = result["id"]
            else:
                # Insert new analyst
                self.cursor.execute('''
                INSERT INTO Analysts (name, organization, expertise, credibility_score)
                VALUES (?, ?, ?, ?)
                ''', (
                    analyst_name,
                    commentary.get("organization", ""),
                    json.dumps(commentary.get("expertise", [])),
                    commentary.get("credibility_score", 0)
                ))
                analyst_id = self.cursor.lastrowid
            
            # Extract classification data
            classification = commentary.get("classification", {})
            primary_category = classification.get("primary_category", "uncategorized")
            priority_score = commentary.get("priority_score", 0)
            
            # Insert commentary
            self.cursor.execute('''
            INSERT INTO AnalystCommentary (
                analyst_id, content, date, source, url, priority_score, primary_category, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                analyst_id,
                commentary.get("content", ""),
                commentary.get("date", ""),
                commentary.get("source", ""),
                commentary.get("url", ""),
                priority_score,
                primary_category,
                datetime.datetime.now().isoformat()
            ))
            
            commentary_id = self.cursor.lastrowid
            
            self.conn.commit()
            logger.info(f"Analyst commentary inserted with ID: {commentary_id}")
            
            return commentary_id
        
        except sqlite3.Error as e:
            logger.error(f"Error inserting analyst commentary: {e}")
            if self.conn:
                self.conn.rollback()
            raise
        
        finally:
            self.close()
    
    def insert_time_series_data(self, metric_name: str, date: str, value: float) -> int:
        """
        Insert time series data into the database
        
        Args:
            metric_name: Name of the metric
            date: Date in ISO format (YYYY-MM-DD)
            value: Metric value
            
        Returns:
            ID of the inserted time series entry
        """
        try:
            self.connect()
            
            # Get metric ID
            self.cursor.execute("SELECT id FROM Metrics WHERE name = ?", (metric_name,))
            result = self.cursor.fetchone()
            
            if not result:
                # Insert new metric
                self.cursor.execute('''
                INSERT INTO Metrics (name, description)
                VALUES (?, ?)
                ''', (metric_name, f"Metric for {metric_name}"))
                metric_id = self.cursor.lastrowid
            else:
                metric_id = result["id"]
            
            # Check if entry already exists for this date and metric
            self.cursor.execute('''
            SELECT id FROM TimeSeries WHERE metric_id = ? AND date = ?
            ''', (metric_id, date))
            result = self.cursor.fetchone()
            
            if result:
                # Update existing entry
                self.cursor.execute('''
                UPDATE TimeSeries SET value = ? WHERE id = ?
                ''', (value, result["id"]))
                time_series_id = result["id"]
            else:
                # Insert new entry
                self.cursor.execute('''
                INSERT INTO TimeSeries (metric_id, date, value)
                VALUES (?, ?, ?)
                ''', (metric_id, date, value))
                time_series_id = self.cursor.lastrowid
            
            self.conn.commit()
            logger.info(f"Time series data inserted with ID: {time_series_id}")
            
            return time_series_id
        
        except sqlite3.Error as e:
            logger.error(f"Error inserting time series data: {e}")
            if self.conn:
                self.conn.rollback()
            raise
        
        finally:
            self.close()
    
    def insert_report(self, report: Dict[str, Any]) -> int:
        """
        Insert a report into the database
        
        Args:
            report: Report data
            
        Returns:
            ID of the inserted report
        """
        try:
            self.connect()
            
            # Insert report
            self.cursor.execute('''
            INSERT INTO Reports (title, content, report_date, report_type, created_at)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                report.get("title", ""),
                json.dumps(report),
                report.get("date", datetime.datetime.now().strftime("%Y-%m-%d")),
                report.get("type", "daily"),
                datetime.datetime.now().isoformat()
            ))
            
            report_id = self.cursor.lastrowid
            
            self.conn.commit()
            logger.info(f"Report inserted with ID: {report_id}")
            
            return report_id
        
        except sqlite3.Error as e:
            logger.error(f"Error inserting report: {e}")
            if self.conn:
                self.conn.rollback()
            raise
        
        finally:
            self.close()
    
    def get_articles_by_category(self, category: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get articles by category
        
        Args:
            category: Category name
            limit: Maximum number of articles to return
            
        Returns:
            List of articles
        """
        try:
            self.connect()
            
            self.cursor.execute('''
            SELECT * FROM Articles
            WHERE primary_category = ?
            ORDER BY priority_score DESC, published_date DESC
            LIMIT ?
            ''', (category, limit))
            
            articles = [dict(row) for row in self.cursor.fetchall()]
            
            return articles
        
        except sqlite3.Error as e:
            logger.error(f"Error getting articles by category: {e}")
            return []
        
        finally:
            self.close()
    
    def get_time_series_data(self, metric_name: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get time series data for a metric
        
        Args:
            metric_name: Name of the metric
            days: Number of days to retrieve
            
        Returns:
            List of time series data points
        """
        try:
            self.connect()
            
            # Calculate date range
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=days)
            
            # Get metric ID
            self.cursor.execute("SELECT id FROM Metrics WHERE name = ?", (metric_name,))
            result = self.cursor.fetchone()
            
            if not result:
                return []
            
            metric_id = result["id"]
            
            # Get time series data
            self.cursor.execute('''
            SELECT date, value FROM TimeSeries
            WHERE metric_id = ? AND date >= ?
            ORDER BY date ASC
            ''', (metric_id, start_date.isoformat()))
            
            data_points = [dict(row) for row in self.cursor.fetchall()]
            
            return data_points
        
        except sqlite3.Error as e:
            logger.error(f"Error getting time series data: {e}")
            return []
        
        finally:
            self.close()
    
    def get_latest_report(self, report_type: str = "daily") -> Optional[Dict[str, Any]]:
        """
        Get the latest report of a specific type
        
        Args:
            report_type: Type of report
            
        Returns:
            Latest report or None if not found
        """
        try:
            self.connect()
            
            self.cursor.execute('''
            SELECT * FROM Reports
            WHERE report_type = ?
            ORDER BY report_date DESC
            LIMIT 1
            ''', (report_type,))
            
            result = self.cursor.fetchone()
            
            if result:
                report = dict(result)
                # Parse JSON content
                report["content"] = json.loads(report["content"])
                return report
            
            return None
        
        except sqlite3.Error as e:
            logger.error(f"Error getting latest report: {e}")
            return None
        
        finally:
            self.close()


# Example usage
if __name__ == "__main__":
    # Create database manager
    db_manager = DatabaseManager()
    
    # Create tables
    db_manager.create_tables()
    
    # Example article
    example_article = {
        "title": "Global Trade Tensions Escalate as US and China Impose New Tariffs",
        "content": "Trade tensions between the United States and China escalated today as both countries announced new tariffs on each other's goods. The move comes amid growing concerns about the global economic outlook and rising geopolitical tensions.",
        "summary": "US and China impose new tariffs amid rising tensions.",
        "url": "https://example.com/article1",
        "published_date": "2023-06-15T10:30:00Z",
        "source": "Financial Times",
        "author": "John Doe",
        "image_url": "https://example.com/image1.jpg",
        "priority_score": 85.5,
        "classification": {
            "primary_category": "external_conflict",
            "secondary_category": "economic_indicators",
            "scores": {
                "internal_conflict": 20.0,
                "external_conflict": 70.0,
                "economic_indicators": 10.0
            }
        }
    }
    
    # Insert example article
    article_id = db_manager.insert_article(example_article)
    
    print(f"Example article inserted with ID: {article_id}")
    
    # Insert time series data
    today = datetime.date.today().isoformat()
    db_manager.insert_time_series_data("external_conflict_count", today, 15)
    db_manager.insert_time_series_data("internal_conflict_count", today, 8)
    db_manager.insert_time_series_data("economic_indicators_count", today, 12)
    
    print("Example time series data inserted")
