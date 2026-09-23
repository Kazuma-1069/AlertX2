from kivymd.uix.card import MDCard
from kivy.properties import StringProperty

class ContactCard(MDCard):
    contact_name = StringProperty("")
    contact_phone = StringProperty("")
    relationship = StringProperty("Friend")
