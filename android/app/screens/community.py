"""
community.py -- Community incident reporting screen for AlertX.
Allows users to submit geo-tagged incident reports and queues them
locally when there is no network connectivity.
"""

import json
import os
from datetime import datetime

from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivy.properties import NumericProperty, StringProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

from app.utils.logger import app_logger

# -- Optional Plyer GPS -------------------------------------------------------
try:
    from plyer import gps as plyer_gps
    _GPS_AVAILABLE = True
except Exception:
    plyer_gps = None
    _GPS_AVAILABLE = False

# -- Constants ----------------------------------------------------------------
API_URL = "http://localhost:8000/api/v1/reports"
PENDING_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "local_data",
)
PENDING_FILE = os.path.join(PENDING_DIR, "pending_reports.json")

REPORT_TYPES = ["ACCIDENT", "FIRE", "ROAD_HAZARD", "UNSAFE_LOCATION", "FLOODING", "OTHER"]


# ---------------------------------------------------------------------------
class CommunityScreen(MDScreen):
    """
    Community incident reporting screen.

    Lets the user choose an incident type, write a description, attach
    their GPS coordinates and POST the report to the backend API.
    Failed submissions are saved to pending_reports.json for later retry.
    """

    latitude = NumericProperty(0.0)
    longitude = NumericProperty(0.0)
    location_text = StringProperty("Location not set")

    # -- Lifecycle ------------------------------------------------------------
    def on_enter(self, *args):
        """Reset form state each time the screen is shown."""
        self._reset_form()
        app_logger.info("CommunityScreen entered.")

    def on_leave(self, *args):
        """Stop GPS when leaving the screen to save battery."""
        self._stop_gps()

    # -- Form helpers ---------------------------------------------------------
    def _reset_form(self):
        """Clear inputs and location back to defaults."""
        try:
            self.ids.report_type_spinner.text = "Select Report Type"
            self.ids.description_input.text = ""
            self.latitude = 0.0
            self.longitude = 0.0
            self.location_text = "Location not set"
            self.ids.location_label.text = "Location not set"
        except Exception as exc:
            app_logger.warning("CommunityScreen._reset_form: %s", exc)

    # -- GPS ------------------------------------------------------------------
    def get_location(self):
        """
        Request the device GPS location.
        Falls back to a snackbar notice if Plyer GPS is unavailable.
        """
        if not _GPS_AVAILABLE or plyer_gps is None:
            app_logger.warning("Plyer GPS not available; using fallback.")
            self._show_snackbar("GPS unavailable on this device.")
            return

        try:
            plyer_gps.configure(
                on_location=self._on_gps_location,
                on_status=self._on_gps_status,
            )
            plyer_gps.start(minTime=1000, minDistance=0)
            self.ids.location_label.text = "Acquiring location..."
            app_logger.info("GPS started.")
            # Auto-stop after 15 s to avoid draining the battery
            Clock.schedule_once(self._stop_gps, 15)
        except Exception as exc:
            app_logger.error("GPS start failed: %s", exc)
            self._show_snackbar("Could not start GPS. Check permissions.")

    def _on_gps_location(self, **kwargs):
        """Callback fired by Plyer when a fix is obtained."""
        self.latitude = float(kwargs.get("lat", 0.0))
        self.longitude = float(kwargs.get("lon", 0.0))
        self.location_text = f"Lat: {self.latitude:.5f}  Lon: {self.longitude:.5f}"
        self.ids.location_label.text = self.location_text
        app_logger.info("GPS fix: %s, %s", self.latitude, self.longitude)
        self._stop_gps()

    def _on_gps_status(self, stype, status):
        app_logger.debug("GPS status: %s - %s", stype, status)

    def _stop_gps(self, *args):
        if _GPS_AVAILABLE and plyer_gps is not None:
            try:
                plyer_gps.stop()
            except Exception as exc:
                app_logger.debug("GPS stop: %s", exc)

    # -- Validation -----------------------------------------------------------
    def _validate(self) -> bool:
        """Return True if the form is ready to submit."""
        spinner_text = self.ids.report_type_spinner.text
        if spinner_text in ("", "Select Report Type"):
            self._show_snackbar("Please select a report type.")
            return False

        description = self.ids.description_input.text.strip()
        if len(description) < 10:
            self._show_snackbar("Please add a description (min 10 characters).")
            return False

        return True

    # -- Submit ---------------------------------------------------------------
    def submit_report(self):
        """Validate the form and POST the report to the API."""
        if not self._validate():
            return

        payload = {
            "type": self.ids.report_type_spinner.text,
            "description": self.ids.description_input.text.strip(),
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        app_logger.info("Submitting report: %s", payload)

        body = json.dumps(payload).encode("utf-8")

        try:
            UrlRequest(
                url=API_URL,
                req_body=body,
                req_headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                on_success=self._on_submit_success,
                on_failure=self._on_submit_failure,
                on_error=self._on_submit_error,
                timeout=10,
                method="POST",
            )
            self.ids.submit_btn.disabled = True
            self.ids.submit_btn.text = "Submitting..."
        except Exception as exc:
            app_logger.error("UrlRequest creation failed: %s", exc)
            self._save_pending(payload)
            self._show_snackbar("No network. Report saved for later.")
            self._re_enable_submit()

    # -- API callbacks --------------------------------------------------------
    def _on_submit_success(self, request, result):
        app_logger.info("Report submitted successfully: %s", result)
        self._show_snackbar(
            "Report submitted. Thank you for keeping your community safe!"
        )
        self._reset_form()
        self._re_enable_submit()

    def _on_submit_failure(self, request, result):
        app_logger.warning("Report submission failed (HTTP %s): %s", request.resp_status, result)
        try:
            payload = json.loads(request.req_body)
        except Exception:
            payload = {}
        self._save_pending(payload)
        self._show_snackbar("Submission failed. Report saved locally for retry.")
        self._re_enable_submit()

    def _on_submit_error(self, request, error):
        app_logger.error("Network error submitting report: %s", error)
        try:
            payload = json.loads(request.req_body)
        except Exception:
            payload = {}
        self._save_pending(payload)
        self._show_snackbar("No network. Report saved for later.")
        self._re_enable_submit()

    def _re_enable_submit(self):
        try:
            self.ids.submit_btn.disabled = False
            self.ids.submit_btn.text = "Submit Report"
        except Exception:
            pass

    # -- Pending queue --------------------------------------------------------
    def _save_pending(self, payload: dict):
        """Append payload to the local pending-reports queue."""
        try:
            os.makedirs(PENDING_DIR, exist_ok=True)
            existing = []
            if os.path.exists(PENDING_FILE):
                with open(PENDING_FILE, "r", encoding="utf-8") as fh:
                    existing = json.load(fh)
            existing.append(payload)
            with open(PENDING_FILE, "w", encoding="utf-8") as fh:
                json.dump(existing, fh, indent=2)
            app_logger.info("Pending report saved. Total pending: %d", len(existing))
        except Exception as exc:
            app_logger.error("Could not save pending report: %s", exc)

    # -- Navigation -----------------------------------------------------------
    def go_back(self):
        self.manager.current = "home"

    # -- UI helpers -----------------------------------------------------------
    def _show_snackbar(self, message: str):
        try:
            snackbar = Snackbar(text=message, snackbar_x="8dp", snackbar_y="8dp")
            snackbar.size_hint_x = 0.95
            snackbar.open()
        except Exception as exc:
            app_logger.warning("Snackbar error: %s", exc)
