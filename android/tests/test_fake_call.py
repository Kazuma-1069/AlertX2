import pytest


def test_fake_call_initial_state():
    try:
        from app.screens.fake_call import FakeCallScreen
    except ModuleNotFoundError:
        pytest.skip("Kivy / KivyMD not installed in current environment")

    screen = FakeCallScreen()
    assert screen.call_active is False
    assert screen.call_seconds == 0
    assert screen.timer_text == "00:00"


def test_fake_call_timer_tick():
    try:
        from app.screens.fake_call import FakeCallScreen
    except ModuleNotFoundError:
        pytest.skip("Kivy / KivyMD not installed in current environment")

    screen = FakeCallScreen()
    screen._tick_timer(1)
    assert screen.call_seconds == 1
    assert screen.timer_text == "00:01"
    
    screen.call_seconds = 65
    screen._tick_timer(1)
    assert screen.call_seconds == 66
    assert screen.timer_text == "01:06"
