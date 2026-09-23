from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.evidence import Evidence
from app.repositories.incident_repository import IncidentRepository


# Alias for backward-compat
IncidentEvidence = Evidence


class EvidenceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.inc_repo = IncidentRepository(db)

    async def add_evidence(
        self,
        incident_id: int,
        evidence_type: str,
        storage_reference: str,
    ) -> Evidence:
        evidence = Evidence(
            incident_id=incident_id,
            type=evidence_type,
            storage_reference=storage_reference,
            upload_status="PENDING",
        )
        self.db.add(evidence)
        await self.db.commit()
        await self.db.refresh(evidence)
        return evidence

    async def get_incident_evidences(self, incident_id: int) -> List[Evidence]:
        stmt = select(Evidence).where(Evidence.incident_id == incident_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
