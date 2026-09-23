from enum import Enum
from typing import Optional, List, Dict, Any
from app.utils.storage import local_store
from app.utils.logger import app_logger

class SOSState(str, Enum):
    SAFE = "SAFE"
    SOS_ACTIVATING = "SOS_ACTIVATING"
    SOS_ACTIVE = "SOS_ACTIVE"
    SOS_RESOLVING = "SOS_RESOLVING"
    SOS_RESOLVED = "SOS_RESOLVED"
    SOS_CANCELLED = "SOS_CANCELLED"

class EmergencyState:
    def __init__(self):
        self.current_state: SOSState = SOSState.SAFE
        self.active_incident_id: Optional[int] = None
        self.active_tracking_token: Optional[str] = None
        self.activation_method: str = "BUTTON"
        self.last_known_lat: float = 30.2672
        self.last_known_lng: float = -97.7431
        self.location_accuracy: float = 4.5
        self.battery_level: int = 94
        self.network_connected: bool = True
        self.audio_recording_active: bool = False
        self.offline_queue: List[Dict[str, Any]] = []

        # Load persisted offline emergency state if app was closed during crisis
        persisted = local_store.get("emergency_state")
        if persisted and persisted.get("state") == SOSState.SOS_ACTIVE:
            self.current_state = SOSState.SOS_ACTIVE
            self.active_incident_id = persisted.get("incident_id")
            self.active_tracking_token = persisted.get("tracking_token")

    @property
    def is_sos_active(self) -> bool:
        return self.is_in_emergency()

    def transition_to(self, new_state: SOSState):
        app_logger.info(f"[SOS State Machine] {self.current_state.value} -> {new_state.value}")
        self.current_state = new_state
        local_store.set("emergency_state", {
            "state": new_state.value,
            "incident_id": self.active_incident_id,
            "tracking_token": self.active_tracking_token
        })

    def is_in_emergency(self) -> bool:
        return self.current_state in (SOSState.SOS_ACTIVATING, SOSState.SOS_ACTIVE)

emergency_state = EmergencyState()
