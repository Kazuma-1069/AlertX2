from app.services.api_client import api_client
from app.state.emergency_state import emergency_state
from app.native.android_location import native_location
from app.native.android_battery import native_battery
from app.utils.logger import app_logger

class SOSService:
    def trigger_sos(self, trigger_type="MANUAL_BUTTON"):
        lat, lng = native_location.get_current_coordinates()
        battery = native_battery.get_battery_level()
        app_logger.info(f"Triggering SOS! Coords: {lat}, {lng}, Trigger: {trigger_type}")
        
        emergency_state.is_sos_active = True
        emergency_state.last_known_lat = lat
        emergency_state.last_known_lng = lng
        
        res = api_client.post("/api/v1/sos/trigger", {
            "latitude": lat,
            "longitude": lng,
            "trigger_type": trigger_type,
            "battery_level": battery
        })
        if "incident_uuid" in res:
            emergency_state.active_incident_uuid = res["incident_uuid"]
        return res

    def cancel_sos(self, reason="User cancelled"):
        if not emergency_state.active_incident_uuid:
            emergency_state.is_sos_active = False
            return {"status": "CANCELLED"}
        res = api_client.post("/api/v1/sos/resolve", {
            "incident_uuid": emergency_state.active_incident_uuid,
            "resolution_notes": reason,
            "status": "CANCELLED"
        })
        emergency_state.is_sos_active = False
        emergency_state.active_incident_uuid = None
        return res

sos_service = SOSService()
