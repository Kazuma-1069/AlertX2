from app.state.emergency_state import emergency_state, SOSState

def test_emergency_state_initial():
    assert emergency_state.is_sos_active is False
    assert emergency_state.current_state == SOSState.SAFE
    assert emergency_state.active_incident_id is None

def test_state_transitions():
    emergency_state.transition_to(SOSState.SOS_ACTIVE)
    assert emergency_state.is_sos_active is True
    emergency_state.transition_to(SOSState.SAFE)
    assert emergency_state.is_sos_active is False
