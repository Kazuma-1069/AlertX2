from kivymd.uix.screen import MDScreen
from app.services.auth_service import auth_service

class AuthScreen(MDScreen):
    def perform_login(self, email, password):
        success = auth_service.login(email, password)
        if success:
            self.manager.current = "home"
