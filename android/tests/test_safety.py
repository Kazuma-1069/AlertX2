from app.models.safety import SafetyTimerModel

def test_safety_timer_model():
    timer = SafetyTimerModel(id=1, title="Night Walk", duration_minutes=20, is_active=True)
    assert timer.duration_minutes == 20
    assert timer.is_active is True
