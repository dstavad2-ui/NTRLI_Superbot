"""
News Module - Business news feed
ANDROID SAFE: Uses lazy imports and safe stubs
"""
import json
from typing import Dict, List
from datetime import datetime
from pathlib import Path


class NewsArticle:
    """News article model"""

    def __init__(self, id: str, title: str, content: str, source: str,
                 published_at: str, category: str = 'business', image_url: str = None):
        self.id = id
        self.title = title
        self.content = content
        self.source = source
        self.published_at = published_at
        self.category = category
        self.image_url = image_url

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'source': self.source,
            'published_at': self.published_at,
            'category': self.category,
            'image_url': self.image_url
        }

    @staticmethod
    def from_dict(data: Dict) -> 'NewsArticle':
        return NewsArticle(**data)


class NewsManager:
    """Manages news feed - Android safe with lazy imports"""

    def __init__(self):
        self.articles: List[NewsArticle] = []
        self.data_dir = Path(__file__).parent.parent / 'data'
        self.data_dir.mkdir(exist_ok=True)

        self.news_file = self.data_dir / 'news.json'
        self.notifications_enabled = True

        self._load_news()

    def _load_news(self):
        """Load cached news from file"""
        if self.news_file.exists():
            try:
                with open(self.news_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.articles = [NewsArticle.from_dict(a) for a in data]
            except Exception as e:
                print(f"Failed to load news: {e}")
                self._create_sample_news()
        else:
            self._create_sample_news()

    def _save_news(self):
        """Save news to file"""
        try:
            with open(self.news_file, 'w', encoding='utf-8') as f:
                json.dump([a.to_dict() for a in self.articles], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save news: {e}")

    def _create_sample_news(self):
        """Create sample news articles"""
        sample_articles = [
            NewsArticle(
                id="NEWS001",
                title="Norway's Economy Shows Strong Growth",
                content="The Norwegian economy continues to show robust growth...",
                source="DN.no",
                published_at=datetime.now().isoformat(),
                category="business"
            ),
            NewsArticle(
                id="NEWS002",
                title="Tech Sector Investments Surge",
                content="Investment in Norway's tech sector has reached record levels...",
                source="E24",
                published_at=datetime.now().isoformat(),
                category="technology"
            ),
            NewsArticle(
                id="NEWS003",
                title="Sustainable Business Practices on the Rise",
                content="Norwegian companies are leading the way in sustainability...",
                source="DN.no",
                published_at=datetime.now().isoformat(),
                category="sustainability"
            )
        ]
        self.articles = sample_articles
        self._save_news()

    def fetch(self) -> List[str]:
        """Simple fetch - returns news titles (Android safe)"""
        return [a.title for a in self.articles]

    def get_news(self, category: str = None, limit: int = 20) -> List[Dict]:
        """Get news articles"""
        articles = self.articles

        if category:
            articles = [a for a in articles if a.category == category]

        articles.sort(key=lambda x: x.published_at, reverse=True)
        articles = articles[:limit]

        return [a.to_dict() for a in articles]

    def get_article(self, article_id: str) -> Dict:
        """Get specific article"""
        for article in self.articles:
            if article.id == article_id:
                return article.to_dict()
        return None

    def refresh_news(self) -> Dict:
        """Refresh news - uses lazy import for aiohttp"""
        try:
            # Lazy import aiohttp only when needed
            import aiohttp
            import asyncio

            async def _fetch():
                # Would fetch from real API here
                return {'success': True, 'count': len(self.articles)}

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(_fetch())
            loop.close()
            return result

        except ImportError:
            print("NewsManager: aiohttp not available, using cached data")
            return {
                'success': True,
                'count': len(self.articles),
                'stub_mode': True
            }

    def enable_notifications(self):
        self.notifications_enabled = True
        return {'success': True}

    def disable_notifications(self):
        self.notifications_enabled = False
        return {'success': True}
