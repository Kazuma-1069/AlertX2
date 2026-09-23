from kivymd.uix.card import MDCard
from kivy.properties import NumericProperty, StringProperty

class LocationCard(MDCard):
    latitude = NumericProperty(0.0)
    longitude = NumericProperty(0.0)
    address = StringProperty("Fetching location...")
