from app.schemas.safety import SafetyTimerCreate

def test_safety_timer_schema():
    timer = SafetyTimerCreate(
        title="Walk Home from Station",
        duration_minutes=15,
        destination_name="Home"
    )
    assert timer.duration_minutes == 15
    assert timer.destination_name == "Home"
