from app.services.api_client import api_client
from app.state.app_state import app_state
from app.utils.storage import local_store

class AuthService:
    def login(self, email, password):
        res = api_client.post("/api/v1/auth/login", {"email": email, "password": password})
        if "access_token" in res:
            app_state.auth_token = res["access_token"]
            app_state.user_id = res.get("user_id")
            app_state.user_name = res.get("full_name", "User")
            app_state.is_authenticated = True
            local_store.set("token", app_state.auth_token)
            return True
        return False

auth_service = AuthService()
