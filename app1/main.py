from kivy.lang import Builder
from kivymd.app import MDApp

KV = '''
Screen:
    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "NTRLI Superbot"
            left_action_items: []  # ✅ No implicit back icon
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
'''

class NTRLISuperbotApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_get_started(self):
        # Add your Get Started logic here
        print("Get Started clicked")

    def on_settings(self):
        # Add your Settings logic here
        print("Settings clicked")

if __name__ == "__main__":
    NTRLISuperbotApp().run()