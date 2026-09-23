from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class SOSTriggerRequest(BaseModel):
    latitude: float
    longitude: float
    accuracy: Optional[float] = None
    activation_method: str = "BUTTON"  # BUTTON, FIVE_TAP, TIMER_EXPIRY
    idempotency_key: Optional[str] = None

class SOSResolveRequest(BaseModel):
    incident_id: int
    resolution_notes: Optional[str] = "Resolved by user"
    status: str = "RESOLVED"  # RESOLVED, CANCELLED

class IncidentEventResponse(BaseModel):
    id: int
    incident_id: int
    event_type: str
    metadata_json: Optional[str] = None
    timestamp: datetime
    class Config:
        from_attributes = True

class SOSIncidentResponse(BaseModel):
    id: int
    user_id: int
    status: str
    activation_method: str
    started_at: datetime
    resolved_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    last_latitude: float
    last_longitude: float
    location_accuracy: Optional[float] = None
    secure_tracking_token: Optional[str] = None
    events: List[IncidentEventResponse] = []
    class Config:
        from_attributes = True
