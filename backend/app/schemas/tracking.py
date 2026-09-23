from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class TrackingSessionResponse(BaseModel):
    id: int
    incident_id: int
    secure_token: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    active: bool
    class Config:
        from_attributes = True

class PublicTrackingView(BaseModel):
    secure_token: str
    status: str
    started_at: datetime
    last_latitude: float
    last_longitude: float
    location_accuracy: Optional[float] = None
    last_updated: datetime
    # Intentionally excludes user_id, private medical info, and internal DB IDs for privacy
