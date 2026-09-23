from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty

class EmergencyBanner(MDBoxLayout):
    message = StringProperty("Emergency Mode Activated")
