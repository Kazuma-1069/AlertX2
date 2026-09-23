from kivymd.uix.screen import MDScreen
from app.services.sos_service import sos_service

class HomeScreen(MDScreen):
    def on_sos_click(self):
        sos_service.trigger_sos()
        self.manager.current = "emergency"
