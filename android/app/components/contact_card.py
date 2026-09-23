from kivymd.uix.card import MDCard
from kivy.properties import NumericProperty, StringProperty, BooleanProperty

class ContactCard(MDCard):
    contact_id = NumericProperty(0)
    contact_name = StringProperty("")
    contact_phone = StringProperty("")
    relationship = StringProperty("Friend")
    priority = NumericProperty(1)
    receive_sos = BooleanProperty(True)
    receive_location = BooleanProperty(True)
