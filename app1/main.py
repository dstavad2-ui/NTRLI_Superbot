"""
NTRLI Superbot - Main Application Entry Point
KivyMD UI with NTRLI' AI Backend Integration
"""

from kivy.lang import Builder
from kivymd.app import MDApp

# Import NTRLI' AI Components
from .core.ntrli_ai_engine import NTRLIAIEngine
from .core.ai_selector import AISelector, TaskType
from .admin_panel.admin_controller import AdminController
from .user_interface.user_controller import UserController
from .config.api_config import APIConfig

KV = '''
Screen:
    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "NTRLI Superbot"
            left_action_items: []
            md_bg_color: 0.2, 0.3, 0.8, 1

        MDLabel:
            text: "Welcome to NTRLI Superbot!"
            halign: "center"
            theme_text_color: "Primary"

        MDRaisedButton:
            text: "Get Started"
            pos_hint: {"center_x": 0.5}
            on_release: app.on_get_started()

        MDRaisedButton:
            text: "Settings"
            pos_hint: {"center_x": 0.5}
            on_release: app.on_settings()

        MDRaisedButton:
            text: "AI Chat"
            pos_hint: {"center_x": 0.5}
            on_release: app.on_ai_chat()
'''


class NTRLISuperbotApp(MDApp):
    """Main NTRLI Superbot Application with AI Integration"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ai_engine = None
        self.user_controller = None

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        """Initialize AI components on app start"""
        # Initialize user-level AI access
        self.ai_engine = NTRLIAIEngine(is_admin=False)
        self.user_controller = UserController(user_id=0, username="app_user")
        print("NTRLI' AI Engine initialized")

    def on_get_started(self):
        print("Get Started clicked")

    def on_settings(self):
        print("Settings clicked")

    def on_ai_chat(self):
        print("AI Chat clicked - NTRLI' AI ready")


if __name__ == "__main__":
    NTRLISuperbotApp().run()
