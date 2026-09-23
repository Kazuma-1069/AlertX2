"""Nearby Emergency Services screen — AlertX."""
import json
from typing import List, Dict

from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.properties import ListProperty

from app.utils.logger import app_logger

# Static dataset of emergency service types shown nearby
# In production these would be fetched from a Places API with the user's GPS coords
EMERGENCY_SERVICE_TYPES = [
    {"name": "Police Station", "icon": "shield-account", "phone": "100", "type": "police"},
    {"name": "Fire Station", "icon": "fire-truck", "phone": "101", "type": "fire"},
    {"name": "Hospital / Ambulance", "icon": "hospital-building", "phone": "108", "type": "medical"},
    {"name": "Women's Helpline", "icon": "human-female", "phone": "1091", "type": "helpline"},
    {"name": "Child Helpline", "icon": "human-child", "phone": "1098", "type": "helpline"},
    {"name": "Disaster Management", "icon": "alert-octagon", "phone": "108", "type": "disaster"},
    {"name": "Coast Guard", "icon": "ferry", "phone": "1554", "type": "coast"},
    {"name": "Roadside Assistance", "icon": "car-wrench", "phone": "1800-180-1522", "type": "road"},
]


class NearbyScreen(MDScreen):
    """Shows nearby emergency services with quick-dial capability."""

    services = ListProperty([])

    def on_enter(self):
        self.services = EMERGENCY_SERVICE_TYPES
        app_logger.info("NearbyScreen: loaded emergency services list")
        self._try_get_location()

    def _try_get_location(self):
        """Attempt GPS location to sort by proximity (graceful fallback)."""
        try:
            from plyer import gps
            gps.configure(on_location=self._on_location, on_status=self._on_status)
            gps.start(minTime=5000, minDistance=0)
        except Exception as e:
            app_logger.warning(f"NearbyScreen: GPS unavailable — {e}")

    def _on_location(self, **kwargs):
        lat = kwargs.get("lat", 0)
        lon = kwargs.get("lon", 0)
        app_logger.info(f"NearbyScreen: location acquired lat={lat} lon={lon}")
        try:
            from plyer import gps
            gps.stop()
        except Exception:
            pass

    def _on_status(self, stype, status):
        app_logger.info(f"NearbyScreen GPS status: {stype} {status}")

    def call_service(self, phone: str, name: str):
        """Initiate phone call to emergency service."""
        app_logger.info(f"NearbyScreen: calling {name} at {phone}")
        try:
            from app.native.android_calls import make_emergency_call
            make_emergency_call(phone)
        except Exception:
            try:
                from plyer import call
                call.makecall(tel=phone)
            except Exception as e:
                app_logger.error(f"NearbyScreen: call failed — {e}")

    def go_back(self):
        self.manager.current = "home"
