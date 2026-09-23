"""Mission-Critical Instant SOS Activation Engine."""
import uuid
import time
from app.state.emergency_state import emergency_state, SOSState
from app.native.android_location import native_location
from app.native.android_battery import native_battery
from app.native.android_calls import native_calls
from app.native.android_sms import native_sms
from app.native.android_recording import native_recording
from app.services.api_client import api_client
from app.utils.logger import app_logger

class SOSService:
    def trigger_sos(self, activation_method="BUTTON") -> dict:
        """Instant SOS execution - strictly NO COUNTDOWN."""
        app_logger.info(f"!!! TRIGGERING INSTANT SOS (Method: {activation_method}) !!!")
        
        # 1. Immediate local state transition
        emergency_state.activation_method = activation_method
        emergency_state.transition_to(SOSState.SOS_ACTIVE)

        # 2. Acquire real GPS coordinates
        lat, lng = native_location.get_current_coordinates()
        emergency_state.last_known_lat = lat
        emergency_state.last_known_lng = lng
        emergency_state.battery_level = native_battery.get_battery_level()

        # 3. Start ambient audio evidence recording
        try:
            native_recording.start_recording("alertx_evidence_incident.mp4")
            emergency_state.audio_recording_active = True
        except Exception as e:
            app_logger.error(f"Failed to start emergency audio: {e}")

        # 4. Generate local client idempotency key
        idempotency_key = f"sos_{int(time.time())}_{uuid.uuid4().hex[:8]}"

        # 5. Immediate Priority 1 Emergency Contact Call
        try:
            native_calls.make_priority_call()
        except Exception as e:
            app_logger.error(f"Priority call error: {e}")

        # 6. Immediate Native Emergency SMS
        try:
            sms_msg = f"EMERGENCY SOS ALERT! AlertX activated. Location: https://maps.google.com/?q={lat},{lng}"
            native_sms.broadcast_emergency_sms(sms_msg)
        except Exception as e:
            app_logger.error(f"Emergency SMS dispatch error: {e}")

        # 7. Asynchronous backend synchronization (with offline queuing)
        payload = {
            "latitude": lat,
            "longitude": lng,
            "accuracy": emergency_state.location_accuracy,
            "activation_method": activation_method,
            "idempotency_key": idempotency_key
        }

        res = api_client.post("/api/v1/sos", payload)
        if "id" in res:
            emergency_state.active_incident_id = res["id"]
            emergency_state.active_tracking_token = res.get("secure_tracking_token")
            app_logger.info(f"SOS Incident synced with backend: ID={res['id']}")
        else:
            app_logger.warning("Backend unreachable: Incident queued locally for retry.")
            emergency_state.offline_queue.append(payload)

        return {"status": "ACTIVE", "incident_id": emergency_state.active_incident_id}

    def resolve_sos(self, notes="Resolved by user", status="RESOLVED") -> dict:
        """Acknowledge safety and terminate active emergency."""
        app_logger.info(f"Terminating SOS (Status: {status})")
        
        # Stop evidence recording
        if emergency_state.audio_recording_active:
            native_recording.stop_recording()
            emergency_state.audio_recording_active = False

        incident_id = emergency_state.active_incident_id
        if incident_id:
            api_client.post("/api/v1/sos/resolve", {
                "incident_id": incident_id,
                "resolution_notes": notes,
                "status": status
            })

        emergency_state.active_incident_id = None
        emergency_state.active_tracking_token = None
        emergency_state.transition_to(SOSState.SOS_RESOLVED if status == "RESOLVED" else SOSState.SOS_CANCELLED)
        emergency_state.transition_to(SOSState.SAFE)
        return {"status": "SAFE"}

sos_service = SOSService()
