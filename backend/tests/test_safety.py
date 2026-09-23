from app.schemas.safety import SafetyTimerCreate

def test_safety_timer_schema():
    timer = SafetyTimerCreate(
        duration_minutes=15,
        title="Walk Home from Station",
        destination="Home"
    )
    assert timer.duration_minutes == 15
    assert timer.destination == "Home"
