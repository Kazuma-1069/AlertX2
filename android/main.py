"""AlertX2 Android Application Entrypoint."""
import os
import sys

from kivy.config import Config
Config.set('graphics', 'width', '390')
Config.set('graphics', 'height', '844')
Config.set('graphics', 'resizable', '1')

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.clock import Clock

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
from app.utils.local_store import local_store

# Lazy imports — only loaded when first accessed to speed up startup
def _get_incident_detail_screen():
    from app.screens.incident_detail import IncidentDetailScreen
    return IncidentDetailScreen

def _get_community_screen():
    from app.screens.community import CommunityScreen
    return CommunityScreen

def _get_fake_call_screen():
    from app.screens.fake_call import FakeCallScreen
    return FakeCallScreen

def _get_guide_detail_screen():
    from app.screens.guide_detail import GuideDetailScreen
    return GuideDetailScreen


class AlertXApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "AlertX"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Dark"

    def build(self):
        app_logger.info("Building AlertX Application...")

        # Load all KV layout files
        kv_dir = os.path.join(os.path.dirname(__file__), "kv")
        if os.path.exists(kv_dir):
            for kv_file in sorted(os.listdir(kv_dir)):
                if kv_file.endswith(".kv"):
                    kv_path = os.path.join(kv_dir, kv_file)
                    try:
                        Builder.load_file(kv_path)
                        app_logger.info(f"Loaded KV: {kv_file}")
                    except Exception as e:
                        app_logger.warning(f"Could not load {kv_file}: {e}")

        sm = ScreenManager(transition=SlideTransition())

        # Core screens
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(OnboardingScreen(name="onboarding"))
        sm.add_widget(AuthScreen(name="auth"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(EmergencyScreen(name="emergency"))

        # Safety
        sm.add_widget(SafetyScreen(name="safety"))

        # Guides
        sm.add_widget(GuidesScreen(name="guides"))
        try:
            GuideDetailScreen = _get_guide_detail_screen()
            sm.add_widget(GuideDetailScreen(name="guide_detail"))
        except Exception as e:
            app_logger.warning(f"GuideDetailScreen unavailable: {e}")

        # Contacts
        sm.add_widget(ContactsScreen(name="contacts"))

        # Profile
        sm.add_widget(ProfileScreen(name="profile"))

        # Incidents + Evidence
        sm.add_widget(IncidentScreen(name="incident"))
        try:
            IncidentDetailScreen = _get_incident_detail_screen()
            sm.add_widget(IncidentDetailScreen(name="incident_detail"))
        except Exception as e:
            app_logger.warning(f"IncidentDetailScreen unavailable: {e}")

        # Community reporting
        try:
            CommunityScreen = _get_community_screen()
            sm.add_widget(CommunityScreen(name="community"))
        except Exception as e:
            app_logger.warning(f"CommunityScreen unavailable: {e}")

        # Fake call
        try:
            FakeCallScreen = _get_fake_call_screen()
            sm.add_widget(FakeCallScreen(name="fake_call"))
        except Exception as e:
            app_logger.warning(f"FakeCallScreen unavailable: {e}")

        # Nearby services
        sm.add_widget(NearbyScreen(name="nearby"))

        # Determine start screen
        onboarded = local_store.get("onboarding_complete", False)
        token = local_store.get("auth_token")

        if not onboarded:
            sm.current = "splash"
        elif token:
            sm.current = "home"
        else:
            sm.current = "auth"

        return sm

    def switch_incident(self, incident_id: int):
        """Navigate to incident detail screen for a given incident id."""
        sm = self.root
        if sm.has_screen("incident_detail"):
            detail = sm.get_screen("incident_detail")
            detail.load_incident(incident_id)
            sm.current = "incident_detail"

    def switch_guide(self, guide_id: str):
        """Navigate to guide detail screen for a given guide id."""
        sm = self.root
        if sm.has_screen("guide_detail"):
            detail = sm.get_screen("guide_detail")
            detail.load_guide(guide_id)
            sm.current = "guide_detail"


if __name__ == "__main__":
    AlertXApp().run()
