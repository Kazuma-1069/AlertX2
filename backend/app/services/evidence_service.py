from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.evidence import IncidentEvidence
from app.repositories.incident_repository import IncidentRepository

class EvidenceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.inc_repo = IncidentRepository(db)

    async def add_evidence(self, incident_uuid: str, file_type: str, file_path: str, size: Optional[int] = None, duration: Optional[int] = None) -> Optional[IncidentEvidence]:
        incident = await self.inc_repo.get_by_uuid(incident_uuid)
        if not incident:
            return None
        evidence = IncidentEvidence(
            incident_id=incident.id,
            file_type=file_type,
            file_path=file_path,
            file_size_bytes=size,
            duration_seconds=duration
        )
        self.db.add(evidence)
        await self.db.commit()
        await self.db.refresh(evidence)
        return evidence

    async def get_incident_evidences(self, incident_uuid: str) -> List[IncidentEvidence]:
        incident = await self.inc_repo.get_by_uuid(incident_uuid)
        if not incident:
            return []
        stmt = select(IncidentEvidence).where(IncidentEvidence.incident_id == incident.id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
