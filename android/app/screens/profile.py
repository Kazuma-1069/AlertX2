"""Profile & Medical Settings Screen matching Stitch profile_sos_settings."""
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, BooleanProperty
from app.services.api_client import api_client

class ProfileScreen(MDScreen):
    blood_group = StringProperty("O+")
    allergies = StringProperty("Penicillin")
    five_tap_enabled = BooleanProperty(True)

    def save_medical(self, blood, allergies):
        api_client.post("/api/v1/users/me/medical", {
            "blood_group": blood,
            "allergies": allergies,
            "is_shared_with_responders": True
        })

    def open_section(self, section_name):
        if self.manager:
            self.manager.current = section_name
