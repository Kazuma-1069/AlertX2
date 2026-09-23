import time
from app.utils.tap_detector import FiveTapDetector

def test_five_tap_detection_success():
    detector = FiveTapDetector(max_interval_seconds=1.5, required_taps=5)
    # Simulate 5 rapid taps within 0.5s
    res = False
    for _ in range(5):
        res = detector.record_tap()
    assert res is True

def test_slow_taps_do_not_trigger_sos():
    detector = FiveTapDetector(max_interval_seconds=0.1, required_taps=5)
    detector.record_tap()
    time.sleep(0.15)
    # Taps separated by more than interval do not trigger
    res = detector.record_tap()
    assert res is False
