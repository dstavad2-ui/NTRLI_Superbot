"""
NTRLI Superbot - Main Application Entry Point
KivyMD UI with NTRLI' AI Backend Integration

IMPORTANT: Uses lazy imports to prevent Android crashes.
Heavy modules are only loaded when needed, not at startup.
"""

from kivy.lang import Builder
from kivymd.app import MDApp

# KV layout - NO implicit icons (prevents drawable crash)
KV = '''
Screen:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "NTRLI Superbot"
            left_action_items: []
            md_bg_color: 0.2, 0.3, 0.8, 1

        MDLabel:
            text: "Welcome to NTRLI Superbot!"
            halign: "center"
            theme_text_color: "Primary"

        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "10dp"
            size_hint_y: None
            height: self.minimum_height
            pos_hint: {"center_x": 0.5}

            MDRaisedButton:
                text: "Get Started"
                size_hint_x: 0.8
                pos_hint: {"center_x": 0.5}
                on_release: app.on_get_started()

            MDRaisedButton:
                text: "Settings"
                size_hint_x: 0.8
                pos_hint: {"center_x": 0.5}
                on_release: app.on_settings()

            MDRaisedButton:
                text: "AI Chat"
                size_hint_x: 0.8
                pos_hint: {"center_x": 0.5}
                on_release: app.on_ai_chat()

            MDRaisedButton:
                text: "News"
                size_hint_x: 0.8
                pos_hint: {"center_x": 0.5}
                on_release: app.on_news()

            MDRaisedButton:
                text: "Shop"
                size_hint_x: 0.8
                pos_hint: {"center_x": 0.5}
                on_release: app.on_shop()
'''


class NTRLISuperbotApp(MDApp):
    """
    Main NTRLI Superbot Application with AI Integration

    Uses lazy imports to prevent Android crashes from heavy dependencies.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Don't initialize heavy components here - use lazy loading
        self._ai_engine = None
        self._user_controller = None

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        """App started - keep lightweight, use lazy loading"""
        print("NTRLI Superbot started")

    # === LAZY LOADING PROPERTIES ===

    @property
    def ai_engine(self):
        """Lazy load AI engine only when needed"""
        if self._ai_engine is None:
            try:
                from core.ntrli_ai_engine import NTRLIAIEngine
                self._ai_engine = NTRLIAIEngine(is_admin=False)
                print("AI Engine loaded")
            except ImportError as e:
                print(f"AI Engine not available: {e}")
                return None
        return self._ai_engine

    @property
    def user_controller(self):
        """Lazy load user controller only when needed"""
        if self._user_controller is None:
            try:
                from user_interface.user_controller import UserController
                self._user_controller = UserController(user_id=0, username="app_user")
                print("User Controller loaded")
            except ImportError as e:
                print(f"User Controller not available: {e}")
                return None
        return self._user_controller

    # === BUTTON HANDLERS (with lazy imports) ===

    def on_get_started(self):
        """Handle Get Started button - lazy load auth"""
        print("Get Started clicked")
        try:
            from modules.auth import TelegramAuth
            auth = TelegramAuth()
            auth.login()
        except ImportError:
            print("Auth module stub active")

    def on_settings(self):
        """Handle Settings button"""
        print("Settings clicked")

    def on_ai_chat(self):
        """Handle AI Chat button - lazy load AI"""
        print("AI Chat clicked")
        if self.ai_engine:
            print("NTRLI' AI ready for chat")
        else:
            print("AI running in stub mode")

    def on_news(self):
        """Handle News button - lazy load news module"""
        print("News clicked")
        try:
            from modules.news import NewsManager
            news = NewsManager()
            items = news.fetch()
            print(f"News items: {items}")
        except ImportError:
            print("News module stub active")

    def on_shop(self):
        """Handle Shop button - lazy load ecommerce module"""
        print("Shop clicked")
        try:
            from modules.ecommerce import EcommerceManager
            shop = EcommerceManager()
            products = shop.list_products()
            print(f"Products: {products}")
        except ImportError:
            print("Ecommerce module stub active")


if __name__ == "__main__":
    NTRLISuperbotApp().run()
