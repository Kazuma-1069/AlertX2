from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class ContactBase(BaseModel):
    name: str
    phone_number: str
    email: Optional[EmailStr] = None
    relationship: str = "Friend"
    is_primary: bool = False
    receive_sms: bool = True
    receive_call: bool = True
    receive_whatsapp: bool = False

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    relationship: Optional[str] = None
    is_primary: Optional[bool] = None
    receive_sms: Optional[bool] = None
    receive_call: Optional[bool] = None
    receive_whatsapp: Optional[bool] = None

class ContactResponse(ContactBase):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        from_attributes = True
