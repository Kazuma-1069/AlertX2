from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import NumericProperty, StringProperty

class TimerWidget(MDBoxLayout):
    time_remaining = NumericProperty(900)  # 15 mins in sec
    timer_title = StringProperty("Safety Countdown")
