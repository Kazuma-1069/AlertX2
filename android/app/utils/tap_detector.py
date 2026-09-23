"""Five-Tap Rapid Hardware/Touch Detector for AlertX."""
import time
from app.utils.logger import app_logger

class FiveTapDetector:
    def __init__(self, max_interval_seconds=1.5, required_taps=5):
        self.max_interval = max_interval_seconds
        self.required_taps = required_taps
        self.tap_timestamps = []

    def record_tap(self) -> bool:
        """Records a tap. Returns True if 5 rapid taps detected within threshold window."""
        now = time.time()
        # Filter out taps older than the window
        self.tap_timestamps = [t for t in self.tap_timestamps if (now - t) <= self.max_interval]
        self.tap_timestamps.append(now)

        app_logger.debug(f"Tap registered: count={len(self.tap_timestamps)}/{self.required_taps}")

        if len(self.tap_timestamps) >= self.required_taps:
            app_logger.warning("ALERT! 5-Tap Rapid SOS condition met!")
            self.tap_timestamps.clear()
            return True
        return False

    def reset(self):
        self.tap_timestamps.clear()

five_tap_detector = FiveTapDetector()
