from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class SafetyGuideCreate(BaseModel):
    category: str
    title: str
    summary: str
    steps: List[str]
    dos: Optional[List[str]] = []
    donts: Optional[List[str]] = []
    emergency_numbers: Optional[List[str]] = []
    icon_name: Optional[str] = "shield-alert"

class SafetyGuideResponse(BaseModel):
    id: int
    category: str
    title: str
    summary: str
    steps_json: str
    dos_and_donts_json: Optional[str] = None
    emergency_numbers_json: Optional[str] = None
    icon_name: str
    created_at: datetime
    class Config:
        from_attributes = True
