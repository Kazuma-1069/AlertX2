from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CommunityReportCreate(BaseModel):
    type: str  # ACCIDENT, FIRE, ROAD_HAZARD, UNSAFE_LOCATION, FLOODING, OTHER
    description: str
    latitude: float
    longitude: float
    media_reference: Optional[str] = None

class CommunityReportResponse(BaseModel):
    id: int
    user_id: int
    type: str
    description: str
    latitude: float
    longitude: float
    media_reference: Optional[str] = None
    status: str
    created_at: datetime
    class Config:
        from_attributes = True
