"""AlertX2 Android Mobile Application Entrypoint."""
import os
import sys

from kivy.config import Config
Config.set('graphics', 'width', '390')
Config.set('graphics', 'height', '844')
Config.set('graphics', 'resizable', '1')

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from app.screens.splash import SplashScreen
from app.screens.onboarding import OnboardingScreen
from app.screens.auth import AuthScreen
from app.screens.home import HomeScreen
from app.screens.emergency import EmergencyScreen
from app.screens.safety import SafetyScreen
from app.screens.guides import GuidesScreen
from app.screens.contacts import ContactsScreen
from app.screens.profile import ProfileScreen
from app.screens.incident import IncidentScreen
from app.screens.nearby import NearbyScreen
from app.utils.logger import app_logger

class AlertXApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "AlertX2"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Dark"

    def build(self):
        app_logger.info("Building AlertX2 Application...")
        
        # Load KV layout files
        kv_dir = os.path.join(os.path.dirname(__file__), "kv")
        if os.path.exists(kv_dir):
            for kv_file in sorted(os.listdir(kv_dir)):
                if kv_file.endswith(".kv"):
                    try:
                        Builder.load_file(os.path.join(kv_dir, kv_file))
                    except Exception as e:
                        app_logger.warning(f"Note loading {kv_file}: {e}")

        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(OnboardingScreen(name="onboarding"))
        sm.add_widget(AuthScreen(name="auth"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(EmergencyScreen(name="emergency"))
        sm.add_widget(SafetyScreen(name="safety"))
        sm.add_widget(GuidesScreen(name="guides"))
        sm.add_widget(ContactsScreen(name="contacts"))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(IncidentScreen(name="incident"))
        sm.add_widget(NearbyScreen(name="nearby"))

        sm.current = "home"
        return sm

if __name__ == "__main__":
    AlertXApp().run()
