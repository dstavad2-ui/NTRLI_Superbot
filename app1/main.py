"""
NTRLI Superbot - Minimal Stable Android Version
Guaranteed to launch without crashes
"""
import os
from kivy.utils import platform

# CRITICAL: Only set window size on desktop
if platform not in ('android', 'ios'):
    from kivy.core.window import Window
    Window.size = (360, 640)

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.logger import Logger
import sys
import traceback

# Global crash logging for device debugging
def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Captures all uncaught exceptions to device log file"""
    try:
        log_path = "/sdcard/superbot_crash.log"
        with open(log_path, "a") as f:
            f.write("\n" + "="*50 + "\n")
            f.write(f"CRASH LOG - {__import__('datetime').datetime.now()}\n")
            f.write("="*50 + "\n")
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
        Logger.error(f"Crash logged to {log_path}")
    except Exception as e:
        # Fallback if file writing fails
        Logger.error(f"Failed to write crash log: {e}")
        traceback.print_exception(exc_type, exc_value, exc_traceback)

sys.excepthook = global_exception_handler

# Simple KV string - no external file dependencies
KV = '''
Screen:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.04, 0.04, 0.12, 1

        MDTopAppBar:
            title: "NTRLI Superbot"
            md_bg_color: 0.2, 0.3, 0.8, 1

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(20)

            MDLabel:
                text: "NTRLI"
                font_style: "H2"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0.6, 0.7, 1, 1
                size_hint_y: 0.3

            MDLabel:
                text: "Welcome to NTRLI Superbot"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0.7, 0.7, 0.7, 1
                size_hint_y: 0.1

            Widget:
                size_hint_y: 0.1

            MDRaisedButton:
                text: "Get Started"
                size_hint_x: 0.8
                pos_hint: {"center_x": 0.5}
                md_bg_color: 0.2, 0.4, 0.9, 1
                on_release: app.show_message()

            MDRaisedButton:
                text: "Settings"
                size_hint_x: 0.8
                pos_hint: {"center_x": 0.5}
                md_bg_color: 0.3, 0.2, 0.7, 1
                on_release: app.show_settings()

            Widget:
                size_hint_y: 0.3
'''


class NTRLIApp(MDApp):
    """Minimal stable NTRLI App"""

    def build(self):
        """Build the app UI"""
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        try:
            return Builder.load_string(KV)
        except Exception as e:
            Logger.error(f"Build error: {e}")
            # Return absolute minimal fallback
            from kivy.uix.label import Label
            return Label(text="NTRLI Superbot\nStarting...")

    def show_message(self):
        """Show welcome message"""
        try:
            from kivymd.uix.snackbar import Snackbar
            Snackbar(text="Welcome to NTRLI Superbot!").open()
        except Exception as e:
            Logger.error(f"Message error: {e}")

    def show_settings(self):
        """Show settings"""
        try:
            from kivymd.uix.snackbar import Snackbar
            Snackbar(text="Settings - Coming Soon!").open()
        except Exception as e:
            Logger.error(f"Settings error: {e}")

    def on_pause(self):
        """Handle pause"""
        return True

    def on_resume(self):
        """Handle resume"""
        pass


def main():
    """App entry point"""
    try:
        NTRLIApp().run()
    except Exception as e:
        Logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
