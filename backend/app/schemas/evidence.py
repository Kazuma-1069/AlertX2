from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class EvidenceCreate(BaseModel):
    incident_id: int
    type: str  # AUDIO, IMAGE, SENSOR
    storage_reference: str


class EvidenceResponse(BaseModel):
    id: int
    incident_id: int
    type: str
    storage_reference: str
    upload_status: str
    created_at: datetime

    class Config:
        from_attributes = True


# Backward-compat aliases
IncidentEvidenceCreate = EvidenceCreate
IncidentEvidenceResponse = EvidenceResponse
