from app.schemas.sos import SOSTriggerRequest

def test_sos_trigger_request():
    req = SOSTriggerRequest(
        latitude=30.2672,
        longitude=-97.7431,
        accuracy=4.5,
        activation_method="BUTTON",
        idempotency_key="test_idemp_key_123"
    )
    assert req.latitude == 30.2672
    assert req.activation_method == "BUTTON"
    assert req.idempotency_key == "test_idemp_key_123"
