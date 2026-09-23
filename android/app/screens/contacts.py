"""Emergency Contacts Screen matching Stitch emergency_contacts_management."""
from kivymd.uix.screen import MDScreen
from kivy.properties import ListProperty
from app.services.api_client import api_client
from app.utils.storage import local_store

class ContactsScreen(MDScreen):
    contacts = ListProperty([])

    def on_enter(self):
        self.load_contacts()

    def load_contacts(self):
        res = api_client.get("/api/v1/contacts")
        if isinstance(res, list):
            self.contacts = res
            local_store.set("emergency_contacts", res)
        else:
            self.contacts = local_store.get("emergency_contacts", [])

    def add_emergency_contact(self, name, phone, priority=1):
        if not name or not phone:
            return
        payload = {
            "name": name,
            "phone": phone,
            "relationship": "Trusted Contact",
            "priority": int(priority),
            "receive_sos": True,
            "receive_location": True,
            "receive_checkin_alert": True
        }
        res = api_client.post("/api/v1/contacts", payload)
        self.load_contacts()

    def open_section(self, section_name):
        if self.manager:
            self.manager.current = section_name
