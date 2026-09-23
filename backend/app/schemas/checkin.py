from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CheckInCreate(BaseModel):
    destination: str
    duration_minutes: int = 30
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class CheckInResponse(BaseModel):
    id: int
    user_id: int
    destination: str
    expected_arrival: datetime
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    class Config:
        from_attributes = True
