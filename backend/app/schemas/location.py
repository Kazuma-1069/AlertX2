from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class LocationBreadcrumbCreate(BaseModel):
    incident_uuid: str
    latitude: float
    longitude: float
    accuracy: Optional[float] = None
    speed: Optional[float] = None
    altitude: Optional[float] = None
    battery_level: Optional[int] = None

class LocationBreadcrumbResponse(BaseModel):
    id: int
    incident_id: int
    latitude: float
    longitude: float
    accuracy: Optional[float] = None
    speed: Optional[float] = None
    altitude: Optional[float] = None
    battery_level: Optional[int] = None
    timestamp: datetime
    class Config:
        from_attributes = True
