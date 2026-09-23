from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class SafetyTimerCreate(BaseModel):
    title: str = "Walking Alone"
    duration_minutes: int
    destination_name: Optional[str] = None
    pin: Optional[str] = None

class SafetyTimerCancelRequest(BaseModel):
    timer_id: int
    pin: Optional[str] = None

class SafetyTimerResponse(BaseModel):
    id: int
    user_id: int
    title: str
    duration_minutes: int
    start_time: datetime
    expires_at: datetime
    is_active: bool
    is_completed: bool
    triggered_sos: bool
    destination_name: Optional[str] = None
    class Config:
        from_attributes = True
