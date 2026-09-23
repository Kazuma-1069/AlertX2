from app.state.emergency_state import emergency_state

def test_emergency_state_initial():
    assert emergency_state.is_sos_active is False
    assert emergency_state.active_incident_uuid is None
