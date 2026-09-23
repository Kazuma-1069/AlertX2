"""Emergency Guides matching Stitch emergency_guides_first_aid."""
from kivymd.uix.screen import MDScreen
from kivy.properties import ListProperty, StringProperty
from app.services.api_client import api_client

class GuidesScreen(MDScreen):
    guides_list = ListProperty([])
    active_category = StringProperty("All")

    def on_enter(self):
        # Fetch offline seed guides
        res = api_client.get("/api/v1/guides")
        if isinstance(res, list):
            self.guides_list = res

    def open_guide_detail(self, guide_title):
        if self.manager and "guide_detail" in self.manager.screen_names:
            detail_screen = self.manager.get_screen("guide_detail")
            detail_screen.load_guide(guide_title)
            self.manager.current = "guide_detail"

    def open_section(self, section_name):
        if self.manager:
            self.manager.current = section_name
