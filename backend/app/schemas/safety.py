from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class SafetyTimerCreate(BaseModel):
    duration_minutes: int  # 5, 15, 30, 60, custom
    title: str = "Walking Alone"
    destination: Optional[str] = None

class SafetyTimerCancelRequest(BaseModel):
    timer_id: int
    pin: Optional[str] = None

class SafetyTimerResponse(BaseModel):
    id: int
    user_id: int
    duration: int
    started_at: datetime
    expires_at: datetime
    status: str
    title: str
    destination: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
