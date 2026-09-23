"""Active Emergency Mode Screen matching Stitch sos_active_emergency_mode."""
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty
from app.services.sos_service import sos_service
from app.native.android_calls import native_calls
from app.state.emergency_state import emergency_state

class EmergencyScreen(MDScreen):
    incident_status_text = StringProperty("DISPATCHING TO 3 CONTACTS")
    current_coords_text = StringProperty("30.2672° N, 97.7431° W (Acc: 4.5m)")
    battery_level = NumericProperty(94)

    def on_pre_enter(self):
        self.current_coords_text = f"{emergency_state.last_known_lat:.4f}° N, {emergency_state.last_known_lng:.4f}° W"
        self.battery_level = emergency_state.battery_level

    def dial_dispatch(self):
        native_calls.dial_number("112")

    def cancel_emergency(self):
        sos_service.resolve_sos(notes="User marked safe via app", status="RESOLVED")
        if self.manager:
            self.manager.current = "home"
