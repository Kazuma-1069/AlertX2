from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class IncidentEvidenceCreate(BaseModel):
    incident_uuid: str
    file_type: str  # AUDIO, IMAGE, SENSOR_LOG
    file_path: str
    file_size_bytes: Optional[int] = None
    duration_seconds: Optional[int] = None
    checksum: Optional[str] = None

class IncidentEvidenceResponse(BaseModel):
    id: int
    incident_id: int
    file_type: str
    file_path: str
    file_size_bytes: Optional[int] = None
    duration_seconds: Optional[int] = None
    created_at: datetime
    class Config:
        from_attributes = True
