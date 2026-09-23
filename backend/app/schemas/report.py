from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class IncidentReportCreate(BaseModel):
    incident_type: str
    title: str
    description: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    is_anonymous: str = "NO"

class IncidentReportResponse(BaseModel):
    id: int
    user_id: int
    incident_type: str
    title: str
    description: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    is_anonymous: str
    created_at: datetime
    class Config:
        from_attributes = True
