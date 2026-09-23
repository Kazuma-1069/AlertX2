import json
import requests
from app.utils.constants import DEFAULT_BACKEND_URL
from app.utils.logger import app_logger
from app.state.app_state import app_state

class APIClient:
    def __init__(self, base_url=DEFAULT_BACKEND_URL):
        self.base_url = base_url

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if app_state.auth_token:
            headers["Authorization"] = f"Bearer {app_state.auth_token}"
        return headers

    def post(self, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        try:
            res = requests.post(url, json=data or {}, headers=self._headers(), timeout=5)
            return res.json()
        except Exception as e:
            app_logger.warning(f"API Error POST {url}: {e}")
            return {"error": str(e)}

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        try:
            res = requests.get(url, params=params or {}, headers=self._headers(), timeout=5)
            return res.json()
        except Exception as e:
            app_logger.warning(f"API Error GET {url}: {e}")
            return {"error": str(e)}

api_client = APIClient()
