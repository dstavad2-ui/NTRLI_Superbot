"""
NTRLI SuperAPK - Main Application Entry Point
Phase 0: Minimal Stable Core with AI Self-Healing
"""
import os
import sys
import traceback
from datetime import datetime
from importlib import import_module
from pathlib import Path

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen

# Crash log path
CRASH_LOG = "/sdcard/superbot_crash.log"
AI_CONSOLE_LOG = "/sdcard/AI_consoles_main.log"

class AIConsole:
    """AI Console Logger with Self-Healing"""
    def __init__(self, log_path):
        self.log_path = log_path
        self.ensure_log_exists()
    
    def ensure_log_exists(self):
        try:
            Path(self.log_path).parent.mkdir(parents=True, exist_ok=True)
            Path(self.log_path).touch(exist_ok=True)
        except Exception as e:
            print(f"AIConsole init error: {e}")
    
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        try:
            with open(self.log_path, "a") as f:
                f.write(log_entry)
            print(log_entry.strip())
        except Exception as e:
            print(f"Log write error: {e}")

class CrashHandler:
    """Global crash handler"""
    @staticmethod
    def log_crash(exc_type, exc_value, exc_traceback):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        crash_info = f"\n{'='*50}\nCRASH REPORT: {timestamp}\n{'='*50}\n"
        crash_info += "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        
        try:
            with open(CRASH_LOG, "a") as f:
                f.write(crash_info)
        except:
            pass
        
        print(crash_info)

# Install crash handler
sys.excepthook = CrashHandler.log_crash

class HomeScreen(MDScreen):
    """Main home screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "home"
        
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)
        
        # Branding
        title = Label(
            text="[b]NTRLI SuperAPK[/b]",
            markup=True,
            font_size="24sp",
            size_hint_y=0.2
        )
        layout.add_widget(title)
        
        subtitle = Label(
            text="AI-Powered Business Platform",
            font_size="16sp",
            size_hint_y=0.1
        )
        layout.add_widget(subtitle)
        
        # Spacer
        layout.add_widget(Label(size_hint_y=0.3))
        
        # Get Started button
        btn_start = MDRaisedButton(
            text="Get Started",
            pos_hint={"center_x": 0.5},
            size_hint=(0.8, None),
            height="50dp",
            md_bg_color=(0.2, 0.6, 1, 1)
        )
        btn_start.bind(on_press=self.on_get_started)
        layout.add_widget(btn_start)
        
        # Settings button
        btn_settings = MDRaisedButton(
            text="Settings",
            pos_hint={"center_x": 0.5},
            size_hint=(0.8, None),
            height="50dp",
            md_bg_color=(0.5, 0.5, 0.5, 1)
        )
        btn_settings.bind(on_press=self.on_settings)
        layout.add_widget(btn_settings)
        
        # Spacer
        layout.add_widget(Label(size_hint_y=0.3))
        
        self.add_widget(layout)
    
    def on_get_started(self, instance):
        app = MDApp.get_running_app()
        app.ai_console.log("Get Started button pressed")
        # Phase 1: Will lazy-load auth module
        print("Get Started pressed - Auth module will load here")
    
    def on_settings(self, instance):
        app = MDApp.get_running_app()
        app.ai_console.log("Settings button pressed")
        print("Settings pressed")

class NTRLIApp(MDApp):
    """Main application class"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ai_console = AIConsole(AI_CONSOLE_LOG)
        self.lazy_modules = {}
        self.ai_console.log("=== NTRLI SuperAPK Initializing ===")
        self.self_healf()
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        
        sm = ScreenManager()
        sm.add_widget(HomeScreen())
        
        self.ai_console.log("UI built successfully - Phase 0 complete")
        return sm
    
    def lazy_load(self, module_name):
        """Lazy load modules on demand"""
        if module_name not in self.lazy_modules:
            try:
                self.lazy_modules[module_name] = import_module(module_name)
                self.ai_console.log(f"Module {module_name} loaded successfully")
            except Exception as e:
                self.ai_console.log(f"Module {module_name} load FAILED: {e}", "ERROR")
                raise
        return self.lazy_modules[module_name]
    
    def self_healf(self):
        """AI Self-Healing - Analyze modules, dependencies, system health"""
        self.ai_console.log("=== SELF_HEALF ROUTINE STARTED ===")
        
        # Phase 0 checks
        modules_to_check = {
            "Phase0": ["kivy", "kivymd"],
            "Phase1": ["modules.auth", "modules.network"],
            "Phase2": ["modules.news", "modules.ecommerce"],
            "Phase3": ["modules.ai", "modules.admin", "modules.i18n"]
        }
        
        for phase, modules in modules_to_check.items():
            self.ai_console.log(f"Checking {phase} modules...")
            for mod in modules:
                try:
                    if mod.startswith("modules."):
                        # Don't actually load yet - just check if file exists
                        mod_file = mod.replace(".", "/") + ".py"
                        if os.path.exists(mod_file):
                            self.ai_console.log(f"  ✓ {mod} file present")
                        else:
                            self.ai_console.log(f"  ✗ {mod} NOT FOUND", "WARNING")
                    else:
                        # Try importing core dependencies
                        import_module(mod)
                        self.ai_console.log(f"  ✓ {mod} available")
                except Exception as e:
                    self.ai_console.log(f"  ✗ {mod} check failed: {e}", "ERROR")
        
        # Log system info
        self.ai_console.log(f"Python version: {sys.version}")
        self.ai_console.log(f"Crash log: {CRASH_LOG}")
        self.ai_console.log(f"AI console log: {AI_CONSOLE_LOG}")
        self.ai_console.log("=== SELF_HEALF ROUTINE COMPLETE ===")
    
    def on_start(self):
        self.ai_console.log("App started successfully")
    
    def on_stop(self):
        self.ai_console.log("App stopped")

if __name__ == "__main__":
    try:
        NTRLIApp().run()
    except Exception as e:
        CrashHandler.log_crash(*sys.exc_info())
        raise