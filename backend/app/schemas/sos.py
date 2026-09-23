from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class SOSTriggerRequest(BaseModel):
    latitude: float
    longitude: float
    address: Optional[str] = None
    trigger_type: str = "MANUAL_BUTTON"  # MANUAL_BUTTON, HARDWARE_KEY, TIMER_EXPIRY
    battery_level: Optional[int] = None
    network_status: Optional[str] = None
    description: Optional[str] = None

class SOSResolveRequest(BaseModel):
    incident_uuid: str
    resolution_notes: Optional[str] = "Resolved by user"
    status: str = "RESOLVED"  # RESOLVED, FALSE_ALARM

class SOSIncidentResponse(BaseModel):
    id: int
    incident_uuid: str
    user_id: int
    trigger_type: str
    status: str
    initial_latitude: float
    initial_longitude: float
    initial_address: Optional[str] = None
    battery_level: Optional[int] = None
    network_status: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None
    class Config:
        from_attributes = True
