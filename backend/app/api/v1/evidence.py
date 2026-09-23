from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.evidence import EvidenceCreate, EvidenceResponse
from app.services.evidence_service import EvidenceService

router = APIRouter()


@router.post("", response_model=EvidenceResponse)
async def upload_evidence(
    evidence_in: EvidenceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = EvidenceService(db)
    evidence = await service.add_evidence(
        incident_id=evidence_in.incident_id,
        evidence_type=evidence_in.type,
        storage_reference=evidence_in.storage_reference,
    )
    return evidence


@router.get("/{incident_id}", response_model=List[EvidenceResponse])
async def list_evidence(
    incident_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = EvidenceService(db)
    return await service.get_incident_evidences(incident_id)
