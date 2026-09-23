from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class MedicalProfileBase(BaseModel):
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    chronic_conditions: Optional[str] = None
    emergency_notes: Optional[str] = None
    physician_name: Optional[str] = None
    physician_phone: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_policy_number: Optional[str] = None

class MedicalProfileCreate(MedicalProfileBase):
    pass

class MedicalProfileResponse(MedicalProfileBase):
    id: int
    user_id: int
    updated_at: datetime
    class Config:
        from_attributes = True

class UserSettingsBase(BaseModel):
    sos_countdown_seconds: int = 5
    enable_fall_detection: bool = False
    enable_shake_trigger: bool = True
    power_button_trigger_count: int = 3
    auto_record_audio_on_sos: bool = True
    share_battery_status: bool = True
    stealth_mode: bool = False

class UserSettingsUpdate(BaseModel):
    sos_countdown_seconds: Optional[int] = None
    enable_fall_detection: Optional[bool] = None
    enable_shake_trigger: Optional[bool] = None
    power_button_trigger_count: Optional[int] = None
    auto_record_audio_on_sos: Optional[bool] = None
    share_battery_status: Optional[bool] = None
    stealth_mode: Optional[bool] = None

class UserSettingsResponse(UserSettingsBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    phone_number: str
    full_name: str
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(BaseModel):
    id: int
    email: str
    phone_number: str
    full_name: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    medical_profile: Optional[MedicalProfileResponse] = None
    settings: Optional[UserSettingsResponse] = None
    class Config:
        from_attributes = True
