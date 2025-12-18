"""
NTRLI Superbot - Android Application
Main Entry Point
"""
import os
import sys
from pathlib import Path

# Set up paths
APP_ROOT = Path(__file__).parent
sys.path.insert(0, str(APP_ROOT))

# Configure Kivy before importing
os.environ['KIVY_NO_CONSOLELOG'] = '0'
os.environ['KIVY_LOG_MODE'] = 'MIXED'

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast

# Import app modules
from modules.auth import AuthManager
from modules.network import NetworkManager
from modules.ai import AIManager
from modules.ecommerce import EcommerceManager
from modules.news import NewsManager
from modules.admin import AdminManager
from modules.i18n import LanguageManager

# Window size for development (remove for production)
Window.size = (360, 640)


class LoginScreen(Screen):
    """Telegram Login Screen"""
    pass


class MainScreen(Screen):
    """Main application screen with navigation"""
    pass


class ProductsScreen(Screen):
    """Products catalog screen"""
    pass


class CartScreen(Screen):
    """Shopping cart screen"""
    pass


class NewsScreen(Screen):
    """News feed screen"""
    pass


class AdminScreen(Screen):
    """Admin panel screen"""
    pass


class SettingsScreen(Screen):
    """Settings and language selection"""
    pass


class NTRLIApp(MDApp):
    """Main Application Class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "NTRLI Superbot"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"

        # Initialize managers
        self.auth = AuthManager()
        self.network = NetworkManager()
        self.ai = AIManager()
        self.ecommerce = EcommerceManager()
        self.news = NewsManager()
        self.admin = AdminManager()
        self.lang = LanguageManager()

        # State
        self.user = None
        self.is_admin = False
        self.anonymous_mode = False

    def build(self):
        """Build the application UI"""
        # Load KV files
        Builder.load_file(str(APP_ROOT / 'ui' / 'login.kv'))
        Builder.load_file(str(APP_ROOT / 'ui' / 'main.kv'))
        Builder.load_file(str(APP_ROOT / 'ui' / 'products.kv'))
        Builder.load_file(str(APP_ROOT / 'ui' / 'cart.kv'))
        Builder.load_file(str(APP_ROOT / 'ui' / 'news.kv'))
        Builder.load_file(str(APP_ROOT / 'ui' / 'admin.kv'))
        Builder.load_file(str(APP_ROOT / 'ui' / 'settings.kv'))

        # Create screen manager
        self.screen_manager = ScreenManager(transition=FadeTransition())
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(MainScreen(name='main'))
        self.screen_manager.add_widget(ProductsScreen(name='products'))
        self.screen_manager.add_widget(CartScreen(name='cart'))
        self.screen_manager.add_widget(NewsScreen(name='news'))
        self.screen_manager.add_widget(AdminScreen(name='admin'))
        self.screen_manager.add_widget(SettingsScreen(name='settings'))

        return self.screen_manager

    def on_start(self):
        """Called when the application starts"""
        # Initialize network (Tor/VPN)
        Clock.schedule_once(self.initialize_network, 0.5)

        # Check if user is already authenticated
        if self.auth.check_session():
            self.user = self.auth.get_user()
            self.is_admin = self.auth.is_admin(self.user)
            self.screen_manager.current = 'main'
        else:
            self.screen_manager.current = 'login'

    def initialize_network(self, dt):
        """Initialize Tor/VPN connection"""
        try:
            self.network.connect()
            toast(self.lang.get('network_connected'))
        except Exception as e:
            toast(f"Network error: {str(e)}")

    def telegram_login(self, phone_or_token):
        """Handle Telegram login"""
        try:
            result = self.auth.telegram_login(phone_or_token)
            if result['success']:
                self.user = result['user']
                self.is_admin = self.auth.is_admin(self.user)

                # Show success message
                toast(self.lang.get('login_success'))

                # Navigate to main screen
                self.screen_manager.current = 'main'
            else:
                self.show_error(result.get('error', 'Login failed'))
        except Exception as e:
            self.show_error(str(e))

    def logout(self):
        """Logout user"""
        self.auth.logout()
        self.user = None
        self.is_admin = False
        self.screen_manager.current = 'login'
        toast(self.lang.get('logged_out'))

    def toggle_mode(self):
        """Toggle between Anonymous and Standard mode"""
        self.anonymous_mode = not self.anonymous_mode
        mode = "Anonymous" if self.anonymous_mode else "Standard"
        toast(f"{mode} Mode Active")

        # Update UI based on mode
        self.update_mode_ui()

    def update_mode_ui(self):
        """Update UI elements based on current mode"""
        # Disable shopping in anonymous mode
        if hasattr(self, 'screen_manager'):
            cart_screen = self.screen_manager.get_screen('cart')
            if self.anonymous_mode:
                cart_screen.disabled = True
            else:
                cart_screen.disabled = False

    def change_language(self, lang_code):
        """Change application language"""
        self.lang.set_language(lang_code)
        toast(f"Language changed to {lang_code}")
        # Refresh current screen to apply new language
        self.refresh_current_screen()

    def refresh_current_screen(self):
        """Refresh current screen to apply language changes"""
        current = self.screen_manager.current
        self.screen_manager.current = current

    def show_error(self, message):
        """Show error dialog"""
        dialog = MDDialog(
            title=self.lang.get('error'),
            text=message,
            buttons=[
                MDRaisedButton(
                    text=self.lang.get('ok'),
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def on_pause(self):
        """Handle app pause (Android lifecycle)"""
        return True

    def on_resume(self):
        """Handle app resume (Android lifecycle)"""
        pass


def main():
    """Application entry point"""
    NTRLIApp().run()


if __name__ == '__main__':
    main()
