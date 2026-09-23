"""
fake_call.py -- Fake incoming-call screen for AlertX.

Simulates a realistic incoming phone call UI so a user can safely
exit a dangerous situation without raising suspicion.
"""

from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivymd.uix.screen import MDScreen

from app.utils.logger import app_logger

# -- Optional Plyer ringtone --------------------------------------------------
try:
    from plyer import ringtone as plyer_ringtone
    _RINGTONE_AVAILABLE = True
except Exception:
    plyer_ringtone = None
    _RINGTONE_AVAILABLE = False

# -- Optional Plyer vibrator --------------------------------------------------
try:
    from plyer import vibrator as plyer_vibrator
    _VIBRATOR_AVAILABLE = True
except Exception:
    plyer_vibrator = None
    _VIBRATOR_AVAILABLE = False

# -- Optional MDApp for local_store -------------------------------------------
try:
    from kivymd.app import MDApp
    _APP_AVAILABLE = True
except Exception:
    _APP_AVAILABLE = False


def _read_contact_name() -> str:
    """Return the configured fake-call contact name, defaulting to 'Mom'."""
    if not _APP_AVAILABLE:
        return "Mom"
    try:
        app = MDApp.get_running_app()
        store = getattr(app, "local_store", None)
        if store is not None and store.exists("fake_call_contact"):
            return str(store.get("fake_call_contact")["name"])
    except Exception as exc:
        app_logger.debug("Could not read fake_call_contact: %s", exc)
    return "Mom"


# ---------------------------------------------------------------------------
class FakeCallScreen(MDScreen):
    """
    Fake incoming-call screen.

    State machine
    -------------
    RINGING -> (Accept) -> ACTIVE -> (End Call) -> back
               (Decline) -> back
    """

    # Kivy observable properties
    caller_name = StringProperty("Mom")
    call_active = BooleanProperty(False)
    call_seconds = NumericProperty(0)
    timer_text = StringProperty("00:00")

    # Private state
    _ring_event = None
    _timer_event = None
    _previous_screen = "home"

    # -- Lifecycle ------------------------------------------------------------
    def on_pre_enter(self, *args):
        """Prepare the screen just before it becomes visible."""
        if self.manager:
            self._previous_screen = self.manager.current
        self.caller_name = _read_contact_name()
        self.call_active = False
        self.call_seconds = 0
        self.timer_text = "00:00"
        app_logger.info("FakeCallScreen: ringing from '%s'", self.caller_name)

    def on_enter(self, *args):
        """Start ringing once the screen is fully visible."""
        self._start_ring()

    def on_leave(self, *args):
        """Always clean up audio / timers when leaving."""
        self._stop_ring()
        self._stop_timer()

    # -- Ring -----------------------------------------------------------------
    def _start_ring(self):
        """Play system ringtone and vibrate if Plyer supports it."""
        if _RINGTONE_AVAILABLE and plyer_ringtone is not None:
            try:
                plyer_ringtone.play()
                app_logger.info("Ringtone started.")
            except Exception as exc:
                app_logger.warning("Could not play ringtone: %s", exc)

        if _VIBRATOR_AVAILABLE and plyer_vibrator is not None:
            try:
                plyer_vibrator.pattern(pattern=(0, 300, 200, 300), repeat=0)
                app_logger.info("Vibrator pattern started.")
            except Exception as exc:
                app_logger.debug("Vibrator error: %s", exc)

    def _stop_ring(self):
        """Stop ringtone and vibrator."""
        if _RINGTONE_AVAILABLE and plyer_ringtone is not None:
            try:
                plyer_ringtone.stop()
            except Exception as exc:
                app_logger.debug("Ringtone stop error: %s", exc)

        if _VIBRATOR_AVAILABLE and plyer_vibrator is not None:
            try:
                plyer_vibrator.cancel()
            except Exception as exc:
                app_logger.debug("Vibrator cancel error: %s", exc)

    # -- Accept / Decline / End -----------------------------------------------
    def accept_call(self):
        """Transition from RINGING -> ACTIVE and start the call timer."""
        if self.call_active:
            return
        self._stop_ring()
        self.call_active = True
        self.call_seconds = 0
        self.timer_text = "00:00"
        self._timer_event = Clock.schedule_interval(self._tick_timer, 1)
        app_logger.info("Fake call accepted.")

    def decline_call(self):
        """Decline the call and navigate back."""
        app_logger.info("Fake call declined.")
        self._stop_ring()
        self._go_back()

    def end_call(self):
        """End an active call and navigate back."""
        app_logger.info("Fake call ended after %d s.", self.call_seconds)
        self._stop_timer()
        self.call_active = False
        self._go_back()

    # -- Timer ----------------------------------------------------------------
    def _tick_timer(self, dt):
        """Increment the call duration counter every second."""
        self.call_seconds += 1
        minutes, seconds = divmod(self.call_seconds, 60)
        self.timer_text = f"{minutes:02d}:{seconds:02d}"

    def _stop_timer(self):
        if self._timer_event is not None:
            try:
                self._timer_event.cancel()
            except Exception:
                pass
            self._timer_event = None

    # -- Navigation -----------------------------------------------------------
    def _go_back(self):
        try:
            self.manager.current = self._previous_screen
        except Exception as exc:
            app_logger.error("FakeCallScreen navigation error: %s", exc)
            try:
                self.manager.current = "home"
            except Exception:
                pass
