"""
News Module
Features:
- Business news feed
- Push notifications
"""
import json
from typing import Dict, List
from datetime import datetime
from pathlib import Path
import asyncio
import aiohttp


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
    """Manages news feed and notifications"""

    def __init__(self):
        self.articles: List[NewsArticle] = []
        self.data_dir = Path(__file__).parent.parent / 'data'
        self.data_dir.mkdir(exist_ok=True)

        self.news_file = self.data_dir / 'news.json'
        self.notifications_enabled = True

        # News sources
        self.news_sources = {
            'newsapi': 'https://newsapi.org/v2/top-headlines',
            'rss_feeds': [
                'https://www.dn.no/rss',
                'https://e24.no/rss'
            ]
        }

        self.load_news()

    def load_news(self):
        """Load cached news from file"""
        if self.news_file.exists():
            try:
                with open(self.news_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.articles = [NewsArticle.from_dict(a) for a in data]
            except Exception as e:
                print(f"Failed to load news: {e}")
                self.create_sample_news()
        else:
            self.create_sample_news()

    def save_news(self):
        """Save news to file"""
        try:
            with open(self.news_file, 'w', encoding='utf-8') as f:
                json.dump([a.to_dict() for a in self.articles], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save news: {e}")

    def create_sample_news(self):
        """Create sample news articles"""
        sample_articles = [
            NewsArticle(
                id="NEWS001",
                title="Norway's Economy Shows Strong Growth",
                content="The Norwegian economy continues to show robust growth with GDP increasing by 2.5% this quarter...",
                source="DN.no",
                published_at=datetime.now().isoformat(),
                category="business",
                image_url="assets/news/economy.jpg"
            ),
            NewsArticle(
                id="NEWS002",
                title="Tech Sector Investments Surge",
                content="Investment in Norway's tech sector has reached record levels, with startups raising over 10 billion NOK...",
                source="E24",
                published_at=datetime.now().isoformat(),
                category="technology",
                image_url="assets/news/tech.jpg"
            ),
            NewsArticle(
                id="NEWS003",
                title="Sustainable Business Practices on the Rise",
                content="Norwegian companies are leading the way in sustainable business practices, with 80% implementing green initiatives...",
                source="DN.no",
                published_at=datetime.now().isoformat(),
                category="sustainability",
                image_url="assets/news/green.jpg"
            )
        ]
        self.articles = sample_articles
        self.save_news()

    async def fetch_news(self, category: str = 'business', country: str = 'no') -> Dict:
        """
        Fetch latest news from external sources
        """
        try:
            # This would normally call NewsAPI or RSS feeds
            # For demo purposes, we'll return sample data

            # Example NewsAPI call:
            # api_key = "your-newsapi-key"
            # url = f"{self.news_sources['newsapi']}?country={country}&category={category}&apiKey={api_key}"
            #
            # async with aiohttp.ClientSession() as session:
            #     async with session.get(url) as response:
            #         if response.status == 200:
            #             data = await response.json()
            #             # Process articles...

            return {
                'success': True,
                'message': 'News fetched successfully',
                'count': len(self.articles)
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_news(self, category: str = None, limit: int = 20) -> List[Dict]:
        """Get news articles"""
        articles = self.articles

        if category:
            articles = [a for a in articles if a.category == category]

        # Sort by published date (newest first)
        articles.sort(key=lambda x: x.published_at, reverse=True)

        # Limit results
        articles = articles[:limit]

        return [a.to_dict() for a in articles]

    def get_article(self, article_id: str) -> Dict:
        """Get specific article"""
        for article in self.articles:
            if article.id == article_id:
                return article.to_dict()
        return None

    def refresh_news(self) -> Dict:
        """Refresh news from sources"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.fetch_news())
        loop.close()
        return result

    def enable_notifications(self):
        """Enable push notifications"""
        self.notifications_enabled = True
        return {'success': True, 'message': 'Notifications enabled'}

    def disable_notifications(self):
        """Disable push notifications"""
        self.notifications_enabled = False
        return {'success': True, 'message': 'Notifications disabled'}

    def send_notification(self, title: str, message: str) -> Dict:
        """
        Send push notification
        On Android, this would use Firebase Cloud Messaging
        """
        if not self.notifications_enabled:
            return {'success': False, 'error': 'Notifications disabled'}

        try:
            # Android notification implementation
            try:
                from jnius import autoclass

                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                NotificationBuilder = autoclass('android.app.Notification$Builder')
                Context = autoclass('android.content.Context')

                notification_service = PythonActivity.mActivity.getSystemService(
                    Context.NOTIFICATION_SERVICE
                )

                builder = NotificationBuilder(PythonActivity.mActivity)
                builder.setContentTitle(title)
                builder.setContentText(message)
                builder.setSmallIcon(PythonActivity.mActivity.getApplicationInfo().icon)

                notification = builder.build()
                notification_service.notify(0, notification)

                return {'success': True, 'message': 'Notification sent'}

            except ImportError:
                # Not on Android, just log
                print(f"Notification: {title} - {message}")
                return {'success': True, 'message': 'Notification logged (desktop mode)'}

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def schedule_news_updates(self, interval_minutes: int = 30):
        """
        Schedule automatic news updates
        """
        # This would use APScheduler or similar
        # For now, just a placeholder
        return {
            'success': True,
            'message': f'News updates scheduled every {interval_minutes} minutes'
        }
