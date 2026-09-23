from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class MedicalProfileBase(BaseModel):
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    medical_information: Optional[str] = None
    physician_name: Optional[str] = None
    physician_phone: Optional[str] = None
    is_shared_with_responders: bool = False

class MedicalProfileCreate(MedicalProfileBase):
    pass

class MedicalProfileResponse(MedicalProfileBase):
    id: int
    user_id: int
    updated_at: datetime
    class Config:
        from_attributes = True

class UserSettingsBase(BaseModel):
    enable_five_tap_sos: bool = True
    enable_fall_detection: bool = False
    enable_shake_trigger: bool = True
    auto_record_audio_on_sos: bool = True
    share_battery_status: bool = True
    stealth_mode: bool = False

class UserSettingsUpdate(BaseModel):
    enable_five_tap_sos: Optional[bool] = None
    enable_fall_detection: Optional[bool] = None
    enable_shake_trigger: Optional[bool] = None
    auto_record_audio_on_sos: Optional[bool] = None
    share_battery_status: Optional[bool] = None
    stealth_mode: Optional[bool] = None

class UserSettingsResponse(UserSettingsBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    is_active: bool
    created_at: datetime
    medical_profile: Optional[MedicalProfileResponse] = None
    settings: Optional[UserSettingsResponse] = None
    class Config:
        from_attributes = True
