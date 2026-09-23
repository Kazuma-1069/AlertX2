from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.evidence import IncidentEvidenceCreate, IncidentEvidenceResponse
from app.services.evidence_service import EvidenceService

router = APIRouter()

@router.post("", response_model=IncidentEvidenceResponse)
async def upload_evidence(evidence_in: IncidentEvidenceCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = EvidenceService(db)
    evidence = await service.add_evidence(
        incident_uuid=evidence_in.incident_uuid,
        file_type=evidence_in.file_type,
        file_path=evidence_in.file_path,
        size=evidence_in.file_size_bytes,
        duration=evidence_in.duration_seconds
    )
    if not evidence:
        raise HTTPException(status_code=404, detail="Incident not found for evidence upload")
    return evidence
