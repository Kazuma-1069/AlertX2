"""5-Tab High Contrast Navigation Bar matching Stitch Design."""
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty

class BottomNavigation(MDBoxLayout):
    current_tab = StringProperty("home")

    def switch_tab(self, screen_manager, tab_name):
        self.current_tab = tab_name
        if screen_manager:
            screen_manager.current = tab_name
