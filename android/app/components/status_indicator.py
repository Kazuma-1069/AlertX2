from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import BooleanProperty, StringProperty

class StatusIndicator(MDBoxLayout):
    is_safe = BooleanProperty(True)
    status_text = StringProperty("SYSTEM ACTIVE • SAFE")
