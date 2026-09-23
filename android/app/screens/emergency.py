from kivymd.uix.screen import MDScreen
from app.services.sos_service import sos_service

class EmergencyScreen(MDScreen):
    def cancel_emergency(self):
        sos_service.cancel_sos()
        self.manager.current = "home"
