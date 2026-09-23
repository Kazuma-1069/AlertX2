from app.native.android_location import native_location
from app.services.api_client import api_client
from app.state.emergency_state import emergency_state

class LocationService:
    def sync_breadcrumb(self):
        if not emergency_state.is_sos_active or not emergency_state.active_incident_uuid:
            return
        lat, lng = native_location.get_current_coordinates()
        api_client.post("/api/v1/location/breadcrumb", {
            "incident_uuid": emergency_state.active_incident_uuid,
            "latitude": lat,
            "longitude": lng
        })

location_service = LocationService()
