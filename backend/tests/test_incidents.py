from app.schemas.incident import IncidentSummary

def test_incident_summary():
    summary = IncidentSummary(
        total_incidents=10,
        active_incidents=1,
        resolved_incidents=9
    )
    assert summary.active_incidents == 1
    assert summary.total_incidents == 10
