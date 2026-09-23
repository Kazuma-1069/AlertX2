from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CheckInCreate(BaseModel):
    status_message: str = "I am safe and arrived at my destination."
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None

class CheckInResponse(BaseModel):
    id: int
    user_id: int
    status_message: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True
