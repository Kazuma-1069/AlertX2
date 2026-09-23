from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class EmergencyContactBase(BaseModel):
    name: str
    phone: str
    relationship: str = "Friend"
    priority: int = 1  # 1, 2, 3...
    receive_sos: bool = True
    receive_location: bool = True
    receive_checkin_alert: bool = True

class EmergencyContactCreate(EmergencyContactBase):
    pass

class EmergencyContactUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    relationship: Optional[str] = None
    priority: Optional[int] = None
    receive_sos: Optional[bool] = None
    receive_location: Optional[bool] = None
    receive_checkin_alert: Optional[bool] = None

class EmergencyContactResponse(EmergencyContactBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Aliases for backward and cross-module compatibility
ContactCreate = EmergencyContactCreate
ContactUpdate = EmergencyContactUpdate
ContactResponse = EmergencyContactResponse
