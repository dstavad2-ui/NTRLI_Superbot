"""
NTRLI SuperAPK - News Module
Phase 2: Business news feed aggregator
"""
import feedparser
import requests
from datetime import datetime
from typing import List, Dict

class NewsManager:
    """Handles business news feed aggregation"""
    
    # Default news sources (RSS feeds)
    DEFAULT_SOURCES = [
        {
            "name": "TechCrunch",
            "url": "https://techcrunch.com/feed/",
            "category": "technology"
        },
        {
            "name": "Reuters Business",
            "url": "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best",
            "category": "business"
        },
        {
            "name": "BBC Business",
            "url": "http://feeds.bbci.co.uk/news/business/rss.xml",
            "category": "business"
        },
        {
            "name": "Hacker News",
            "url": "https://news.ycombinator.com/rss",
            "category": "technology"
        },
        {
            "name": "The Verge",
            "url": "https://www.theverge.com/rss/index.xml",
            "category": "technology"
        }
    ]
    
    def __init__(self, ai_console=None, network_manager=None):
        self.ai_console = ai_console
        self.network_manager = network_manager
        self.sources = self.DEFAULT_SOURCES.copy()
        self.cache = []
        self.log("NewsManager initialized")
    
    def log(self, msg, level="INFO"):
        if self.ai_console:
            self.ai_console.log(f"[NEWS] {msg}", level)
        else:
            print(f"[NEWS] {msg}")
    
    def add_source(self, name, url, category="general"):
        """Add custom news source"""
        source = {"name": name, "url": url, "category": category}
        self.sources.append(source)
        self.log(f"Added news source: {name}")
        return True
    
    def remove_source(self, name):
        """Remove news source"""
        self.sources = [s for s in self.sources if s["name"] != name]
        self.log(f"Removed news source: {name}")
        return True
    
    def fetch_feed(self, source):
        """Fetch articles from a single RSS feed"""
        try:
            self.log(f"Fetching feed: {source['name']}")
            
            # Use network manager if available
            if self.network_manager:
                success, response = self.network_manager.make_request(
                    source["url"],
                    timeout=15
                )
                if not success:
                    raise Exception(f"Network request failed: {response}")
                feed_data = response.text
            else:
                response = requests.get(source["url"], timeout=15)
                feed_data = response.text
            
            # Parse RSS feed
            feed = feedparser.parse(feed_data)
            
            articles = []
            for entry in feed.entries[:10]:  # Limit to 10 articles per source
                article = {
                    "title": entry.get("title", "No title"),
                    "summary": entry.get("summary", entry.get("description", "No summary")),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", "Unknown date"),
                    "source": source["name"],
                    "category": source["category"]
                }
                articles.append(article)
            
            self.log(f"Fetched {len(articles)} articles from {source['name']}")
            return articles
        
        except Exception as e:
            self.log(f"Failed to fetch {source['name']}: {e}", "ERROR")
            return []
    
    def fetch_all_feeds(self, category=None):
        """Fetch articles from all sources"""
        all_articles = []
        
        sources_to_fetch = self.sources
        if category:
            sources_to_fetch = [s for s in self.sources if s["category"] == category]
        
        self.log(f"Fetching from {len(sources_to_fetch)} sources...")
        
        for source in sources_to_fetch:
            articles = self.fetch_feed(source)
            all_articles.extend(articles)
        
        # Sort by date (newest first) - best effort
        try:
            all_articles.sort(
                key=lambda x: datetime.strptime(x["published"], "%a, %d %b %Y %H:%M:%S %z"),
                reverse=True
            )
        except:
            # If date parsing fails, just keep original order
            pass
        
        self.cache = all_articles
        self.log(f"Total articles fetched: {len(all_articles)}")
        return all_articles
    
    def get_cached_articles(self, limit=50, category=None):
        """Get cached articles"""
        articles = self.cache
        
        if category:
            articles = [a for a in articles if a["category"] == category]
        
        return articles[:limit]
    
    def search_articles(self, query, limit=20):
        """Search articles by keyword"""
        query = query.lower()
        results = []
        
        for article in self.cache:
            title_match = query in article["title"].lower()
            summary_match = query in article["summary"].lower()
            
            if title_match or summary_match:
                results.append(article)
        
        self.log(f"Search '{query}': {len(results)} results")
        return results[:limit]
    
    def get_categories(self):
        """Get list of available categories"""
        categories = set(s["category"] for s in self.sources)
        return sorted(list(categories))
    
    def get_article_summary(self, article_url):
        """Fetch and extract article content"""
        try:
            if self.network_manager:
                success, response = self.network_manager.make_request(
                    article_url,
                    timeout=10
                )
                if not success:
                    return None, f"Failed to fetch: {response}"
            else:
                response = requests.get(article_url, timeout=10)
            
            # Basic HTML parsing - just get text
            html = response.text
            # Simple text extraction (proper parsing would need BeautifulSoup)
            text = html[:2000]  # First 2000 chars
            
            self.log(f"Fetched article content: {article_url[:50]}...")
            return text, None
        
        except Exception as e:
            self.log(f"Failed to fetch article: {e}", "ERROR")
            return None, str(e)