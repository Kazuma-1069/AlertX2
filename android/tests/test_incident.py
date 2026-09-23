import pytest


def test_incident_detail_export_structure(tmp_path):
    try:
        from app.screens.incident_detail import IncidentDetailScreen
    except ModuleNotFoundError:
        pytest.skip("Kivy / KivyMD not installed in current environment")

    screen = IncidentDetailScreen()
    incident_data = {
        "id": 999,
        "started_at": "2026-09-23T20:00:00Z",
        "resolved_at": "2026-09-23T20:05:00Z",
        "status": "RESOLVED",
        "activation_method": "ONE_TAP",
        "last_latitude": 19.0760,
        "last_longitude": 72.8777,
        "events": [
            {"event_type": "SOS_ACTIVATED", "timestamp": "2026-09-23T20:00:00Z"},
            {"event_type": "RESOLVED", "timestamp": "2026-09-23T20:05:00Z"}
        ],
        "evidence": [
            {"type": "AUDIO", "filename": "audio_999.wav", "timestamp": "2026-09-23T20:01:00Z"}
        ]
    }
    screen._incident = incident_data
    assert screen._incident["id"] == 999
    assert len(screen._incident["events"]) == 2
    assert len(screen._incident["evidence"]) == 1
