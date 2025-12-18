"""
NTRLI Superbot - Android Application
Main Entry Point - Android Optimized
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

# CRITICAL: Import kivy modules first
from kivy.utils import platform
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
from kivy.logger import Logger

# REMOVED: Window.size - causes crashes on Android!
# Only set window size on desktop
if platform not in ('android', 'ios'):
    from kivy.core.window import Window
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

        # Initialize managers lazily to avoid startup crashes
        self.auth = None
        self.network = None
        self.ai = None
        self.ecommerce = None
        self.news = None
        self.admin = None
        self.lang = None

        # State
        self.user = None
        self.is_admin = False
        self.anonymous_mode = False

    def build(self):
        """Build the application UI"""
        try:
            # Load KV files with error handling
            kv_files = ['login', 'main', 'products', 'cart', 'news', 'admin', 'settings']

            for kv_file in kv_files:
                try:
                    kv_path = str(APP_ROOT / 'ui' / f'{kv_file}.kv')
                    Logger.info(f"Loading KV file: {kv_path}")
                    Builder.load_file(kv_path)
                except Exception as e:
                    Logger.error(f"Failed to load {kv_file}.kv: {e}")
                    # Continue even if KV file fails

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

        except Exception as e:
            Logger.error(f"Build error: {e}")
            # Return minimal UI on error
            from kivy.uix.label import Label
            return Label(text=f"Error building app: {str(e)}")

    def on_start(self):
        """Called when the application starts"""
        try:
            # Initialize managers after app starts
            self._init_managers()

            # Initialize network (Tor/VPN) if available
            if self.network:
                Clock.schedule_once(self.initialize_network, 0.5)

            # Check if user is already authenticated
            if self.auth and self.auth.check_session():
                self.user = self.auth.get_user()
                self.is_admin = self.auth.is_admin(self.user)
                self.screen_manager.current = 'main'
            else:
                self.screen_manager.current = 'login'

        except Exception as e:
            Logger.error(f"Startup error: {e}")
            toast("App started with limited functionality")

    def _init_managers(self):
        """Initialize managers with error handling"""
        try:
            from modules.i18n import LanguageManager
            self.lang = LanguageManager()
        except Exception as e:
            Logger.error(f"Failed to load language manager: {e}")

        try:
            from modules.auth import AuthManager
            self.auth = AuthManager()
        except Exception as e:
            Logger.error(f"Failed to load auth manager: {e}")

        try:
            from modules.network import NetworkManager
            self.network = NetworkManager()
        except Exception as e:
            Logger.error(f"Failed to load network manager: {e}")

        try:
            from modules.ai import AIManager
            self.ai = AIManager()
        except Exception as e:
            Logger.error(f"Failed to load AI manager: {e}")

        try:
            from modules.ecommerce import EcommerceManager
            self.ecommerce = EcommerceManager()
        except Exception as e:
            Logger.error(f"Failed to load ecommerce manager: {e}")

        try:
            from modules.news import NewsManager
            self.news = NewsManager()
        except Exception as e:
            Logger.error(f"Failed to load news manager: {e}")

        try:
            from modules.admin import AdminManager
            self.admin = AdminManager()
        except Exception as e:
            Logger.error(f"Failed to load admin manager: {e}")

    def initialize_network(self, dt):
        """Initialize Tor/VPN connection"""
        try:
            if self.network:
                self.network.connect()
                if self.lang:
                    toast(self.lang.get('network_connected'))
                else:
                    toast("Network connected")
        except Exception as e:
            Logger.error(f"Network initialization error: {e}")
            toast(f"Network error: {str(e)}")

    def telegram_login(self, phone_or_token):
        """Handle Telegram login"""
        try:
            if not self.auth:
                toast("Authentication not available")
                return

            result = self.auth.telegram_login(phone_or_token)
            if result['success']:
                self.user = result['user']
                self.is_admin = self.auth.is_admin(self.user)

                # Show success message
                msg = self.lang.get('login_success') if self.lang else "Login successful"
                toast(msg)

                # Navigate to main screen
                self.screen_manager.current = 'main'
            else:
                self.show_error(result.get('error', 'Login failed'))
        except Exception as e:
            Logger.error(f"Login error: {e}")
            self.show_error(str(e))

    def logout(self):
        """Logout user"""
        try:
            if self.auth:
                self.auth.logout()
            self.user = None
            self.is_admin = False
            self.screen_manager.current = 'login'
            msg = self.lang.get('logged_out') if self.lang else "Logged out"
            toast(msg)
        except Exception as e:
            Logger.error(f"Logout error: {e}")

    def toggle_mode(self):
        """Toggle between Anonymous and Standard mode"""
        self.anonymous_mode = not self.anonymous_mode
        mode = "Anonymous" if self.anonymous_mode else "Standard"
        toast(f"{mode} Mode Active")
        self.update_mode_ui()

    def update_mode_ui(self):
        """Update UI elements based on current mode"""
        try:
            if hasattr(self, 'screen_manager'):
                cart_screen = self.screen_manager.get_screen('cart')
                cart_screen.disabled = self.anonymous_mode
        except Exception as e:
            Logger.error(f"Mode update error: {e}")

    def change_language(self, lang_code):
        """Change application language"""
        try:
            if self.lang:
                self.lang.set_language(lang_code)
            toast(f"Language changed to {lang_code}")
            self.refresh_current_screen()
        except Exception as e:
            Logger.error(f"Language change error: {e}")

    def refresh_current_screen(self):
        """Refresh current screen to apply language changes"""
        try:
            current = self.screen_manager.current
            self.screen_manager.current = current
        except Exception as e:
            Logger.error(f"Screen refresh error: {e}")

    def show_error(self, message):
        """Show error dialog"""
        try:
            title = self.lang.get('error') if self.lang else "Error"
            ok_text = self.lang.get('ok') if self.lang else "OK"

            dialog = MDDialog(
                title=title,
                text=message,
                buttons=[
                    MDRaisedButton(
                        text=ok_text,
                        on_release=lambda x: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
        except Exception as e:
            Logger.error(f"Error dialog failed: {e}")
            toast(f"Error: {message}")

    def on_pause(self):
        """Handle app pause (Android lifecycle)"""
        return True

    def on_resume(self):
        """Handle app resume (Android lifecycle)"""
        pass


def main():
    """Application entry point"""
    try:
        NTRLIApp().run()
    except Exception as e:
        Logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
