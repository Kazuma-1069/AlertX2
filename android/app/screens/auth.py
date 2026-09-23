"""Full Auth screen — login + register with API integration."""
import json
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock

from app.utils.local_store import local_store
from app.utils.logger import app_logger
from app.utils.constants import API_BASE_URL


class AuthScreen(MDScreen):
    """Login and registration screen with real API integration."""

    def on_enter(self):
        # Auto-login if token is stored
        token = local_store.get("auth_token")
        if token:
            app_logger.info("AuthScreen: auto-login via stored token")
            Clock.schedule_once(lambda dt: self._go_home(), 0.1)

    def perform_login(self, email: str, password: str):
        """Validate inputs and POST /auth/login."""
        email = email.strip()
        password = password.strip()

        if not email or not password:
            self._show_error("Email and password are required")
            return

        if "@" not in email:
            self._show_error("Enter a valid email address")
            return

        body = json.dumps({"email": email, "password": password})
        UrlRequest(
            url=f"{API_BASE_URL}/api/v1/auth/login",
            req_body=body,
            req_headers={"Content-Type": "application/json"},
            on_success=self._on_login_success,
            on_failure=self._on_login_failure,
            on_error=self._on_login_error,
            timeout=10,
        )
        app_logger.info(f"AuthScreen: login attempt for {email}")

    def perform_register(self, name: str, email: str, phone: str, password: str):
        """Validate inputs and POST /auth/register."""
        name = name.strip()
        email = email.strip()
        phone = phone.strip()
        password = password.strip()

        if not all([name, email, phone, password]):
            self._show_error("All fields are required")
            return

        if len(password) < 8:
            self._show_error("Password must be at least 8 characters")
            return

        if "@" not in email:
            self._show_error("Enter a valid email address")
            return

        body = json.dumps({
            "name": name,
            "email": email,
            "phone": phone,
            "password": password,
        })
        UrlRequest(
            url=f"{API_BASE_URL}/api/v1/auth/register",
            req_body=body,
            req_headers={"Content-Type": "application/json"},
            on_success=self._on_register_success,
            on_failure=self._on_register_failure,
            on_error=self._on_login_error,
            timeout=10,
        )
        app_logger.info(f"AuthScreen: register attempt for {email}")

    # ── Callbacks ──────────────────────────────────────────────────────────

    def _on_login_success(self, request, result):
        token = result.get("access_token")
        if token:
            local_store.set("auth_token", token)
            local_store.set("user_email", result.get("email", ""))
            app_logger.info("AuthScreen: login successful")
            self._go_home()
        else:
            self._show_error("Login failed — invalid response")

    def _on_login_failure(self, request, result):
        detail = result.get("detail", "Login failed") if isinstance(result, dict) else "Login failed"
        self._show_error(str(detail))
        app_logger.warning(f"AuthScreen: login failure — {detail}")

    def _on_login_error(self, request, error):
        self._show_error("Cannot reach server. Check your connection.")
        app_logger.error(f"AuthScreen: network error — {error}")

    def _on_register_success(self, request, result):
        app_logger.info("AuthScreen: registration successful")
        self._show_snackbar("Account created! Please log in.")

    def _on_register_failure(self, request, result):
        detail = result.get("detail", "Registration failed") if isinstance(result, dict) else "Registration failed"
        self._show_error(str(detail))
        app_logger.warning(f"AuthScreen: register failure — {detail}")

    # ── Helpers ────────────────────────────────────────────────────────────

    def _go_home(self):
        self.manager.current = "home"

    def _show_error(self, message: str):
        self._show_snackbar(message)

    def _show_snackbar(self, message: str):
        try:
            Snackbar(text=message, snackbar_x="8dp", snackbar_y="8dp",
                     size_hint_x=(1 - 16 / 390)).open()
        except Exception:
            app_logger.error(f"AuthScreen snackbar: {message}")
