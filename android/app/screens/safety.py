"""Safety Screen matching Stitch safety_tools_timer."""
from kivymd.uix.screen import MDScreen
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from app.services.safety_service import safety_service
from app.native.android_calls import native_calls
from app.utils.logger import app_logger

class SafetyScreen(MDScreen):
    timer_seconds = NumericProperty(0)
    timer_active = BooleanProperty(False)
    timer_display = StringProperty("15:00")
    active_timer_id = NumericProperty(0)
    destination_text = StringProperty("Walking Home")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._timer_event = None

    def start_preset_timer(self, minutes: int):
        self.timer_seconds = minutes * 60
        self.timer_active = True
        self.update_display()
        app_logger.info(f"Starting {minutes}-min safety timer")
        
        # Async sync with backend
        res = safety_service.start_timer(self.destination_text, minutes)
        if "id" in res:
            self.active_timer_id = res["id"]

        if self._timer_event:
            self._timer_event.cancel()
        self._timer_event = Clock.schedule_interval(self._tick, 1.0)

    def _tick(self, dt):
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.update_display()
        else:
            self._timer_event.cancel()
            self.timer_active = False
            self.on_timer_expired()

    def update_display(self):
        mins = self.timer_seconds // 60
        secs = self.timer_seconds % 60
        self.timer_display = f"{mins:02d}:{secs:02d}"

    def cancel_timer(self):
        if self._timer_event:
            self._timer_event.cancel()
        self.timer_active = False
        self.timer_seconds = 0
        self.timer_display = "00:00"
        if self.active_timer_id:
            safety_service.cancel_timer(self.active_timer_id)
        app_logger.info("Safety timer cancelled by user: I AM SAFE")

    def on_timer_expired(self):
        app_logger.warning("SAFETY TIMER EXPIRED! Auto-escalating to emergency contacts!")
        # Auto-escalation trigger
        from app.services.sos_service import sos_service
        sos_service.trigger_sos(activation_method="TIMER_EXPIRY")
        if self.manager:
            self.manager.current = "emergency"

    def trigger_fake_call(self):
        app_logger.info("Scheduling simulated fake incoming call in 5 seconds...")
        Clock.schedule_once(lambda dt: self._launch_fake_call(), 5.0)

    def _launch_fake_call(self):
        if self.manager and "fake_call" in self.manager.screen_names:
            self.manager.current = "fake_call"
        else:
            app_logger.info("INCOMING FAKE CALL: Mom (+1 555-0192) Calling...")

    def open_section(self, section_name):
        if self.manager:
            self.manager.current = section_name
