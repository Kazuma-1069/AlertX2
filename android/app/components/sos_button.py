from kivymd.uix.button import MDFillRoundFlatButton
from kivy.properties import BooleanProperty
from app.services.sos_service import sos_service

class SOSButton(MDFillRoundFlatButton):
    is_pressed = BooleanProperty(False)

    def trigger(self):
        sos_service.trigger_sos(trigger_type="MANUAL_BUTTON")
