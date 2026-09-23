from app.schemas.sos import SOSTriggerRequest

def test_sos_trigger_request():
    req = SOSTriggerRequest(
        latitude=37.7749,
        longitude=-122.4194,
        trigger_type="MANUAL_BUTTON",
        battery_level=85
    )
    assert req.latitude == 37.7749
    assert req.trigger_type == "MANUAL_BUTTON"
