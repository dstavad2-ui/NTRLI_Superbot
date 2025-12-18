from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
import traceback, sys, os

# LOG PATHS
CRASH_LOG = "/sdcard/superbot_crash.log"
AI_LOG = "/sdcard/ai_logs.txt"

# LOGGING HELPERS
def write_crash(e):
    try:
        with open(CRASH_LOG, "a") as f:
            f.write(traceback.format_exc() + "\n")
    except:
        pass

def ai_console_log(tag, msg):
    try:
        with open(AI_LOG, "a") as f:
            f.write(f"[{tag}] {msg}\n")
    except:
        pass

# GLOBAL EXCEPTION HOOK
def global_excepthook(exc_type, exc_value, exc_tb):
    write_crash(exc_value)
    ai_console_log("GLOBAL_CRASH", str(exc_value))

sys.excepthook = global_excepthook

# SELF HEAL DIAGNOSTIC
def self_healf():
    ai_console_log("SELF_HEAL", "Running self_healf checks")
    for m in ["modules.news", "modules.ecommerce", "modules.admin", "modules.i18n"]:
        try:
            __import__(m)
            ai_console_log("SELF_HEAL_OK", f"{m} loaded")
        except Exception as e:
            ai_console_log("SELF_HEAL_FAIL", f"{m}: {e}")

KV = '''
BoxLayout:
    orientation: "vertical"

    MDToolbar:
        title: "NTRLI SuperAPK"
        left_action_items: []

    MDRaisedButton:
        text: "Get Started"
        on_release: app.on_get_started()

    MDRaisedButton:
        text: "Settings"
        on_release: app.on_settings()

    MDRaisedButton:
        text: "Run Self Heal"
        on_release: app.on_self_healf()
'''

class NTRLIApp(MDApp):
    def build(self):
        self.self_healf()  # call on startup
        return Builder.load_string(KV)

    def on_get_started(self):
        try:
            Snackbar(text="Phase 0 Active").open()
            ai_console_log("UI", "Get Started clicked")
        except Exception as e:
            write_crash(e)

    def on_settings(self):
        try:
            Snackbar(text="Settings clicked").open()
            ai_console_log("UI", "Settings clicked")
        except Exception as e:
            write_crash(e)

    def on_self_healf(self):
        try:
            self_healf()
            Snackbar(text="Self Heal Completed").open()
        except Exception as e:
            write_crash(e)

if __name__ == "__main__":
    try:
        NTRLIApp().run()
    except Exception as e:
        write_crash(e)