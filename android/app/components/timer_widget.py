from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import NumericProperty, StringProperty

class TimerWidget(MDBoxLayout):
    seconds_remaining = NumericProperty(900)
    title = StringProperty("Walking Home Alone")
    destination = StringProperty("")
