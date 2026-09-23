from app.schemas.location import LocationBreadcrumbCreate

def test_breadcrumb_payload():
    crumb = LocationBreadcrumbCreate(
        incident_uuid="test-uuid-1234",
        latitude=37.7749,
        longitude=-122.4194,
        accuracy=5.2,
        battery_level=90
    )
    assert crumb.incident_uuid == "test-uuid-1234"
    assert crumb.accuracy == 5.2
