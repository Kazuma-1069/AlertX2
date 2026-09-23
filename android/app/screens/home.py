"""Home Screen matching Stitch design home_sos_ready."""
from kivymd.uix.screen import MDScreen
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from app.services.sos_service import sos_service
from app.utils.tap_detector import five_tap_detector
from app.utils.logger import app_logger

class HomeScreen(MDScreen):
    is_five_tap_enabled = BooleanProperty(True)
    battery_text = StringProperty("Battery 94%")
    location_text = StringProperty("Lat 30.2672° N, Long 97.7431° W")

    def on_touch_down(self, touch):
        # 5-Tap detector evaluates any rapid taps on the screen
        if self.is_five_tap_enabled and five_tap_detector.record_tap():
            app_logger.warning("5-Tap Rapid SOS Triggered from HomeScreen touch events!")
            self.trigger_emergency(activation_method="FIVE_TAP")
            return True
        return super().on_touch_down(touch)

    def trigger_emergency(self, activation_method="BUTTON"):
        sos_service.trigger_sos(activation_method=activation_method)
        if self.manager:
            self.manager.current = "emergency"

    def open_section(self, section_name):
        if self.manager:
            self.manager.current = section_name
