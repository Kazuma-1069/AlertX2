from kivymd.uix.card import MDCard
from kivy.properties import StringProperty

class GuideCard(MDCard):
    title = StringProperty("")
    category = StringProperty("")
    summary = StringProperty("")
