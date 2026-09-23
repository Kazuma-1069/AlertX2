"""Tactical SOS Button matching Stitch Design."""
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.behaviors import TouchBehavior
from app.services.sos_service import sos_service
from app.utils.logger import app_logger

class SOSButton(MDFillRoundFlatButton, TouchBehavior):
    is_pressed = BooleanProperty(False)
    hold_time = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "SOS"
        self.font_size = "40sp"
        self.size_hint = (None, None)
        self.size = ("140dp", "140dp")
        self.md_bg_color = (0.851, 0.176, 0.125, 1.0)  # #D92D20

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # One-tap immediate SOS activation
            app_logger.info("SOS Button clicked: triggering instant emergency sequence")
            sos_service.trigger_sos(activation_method="BUTTON")
            return True
        return super().on_touch_down(touch)
