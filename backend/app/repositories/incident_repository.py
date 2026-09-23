from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.sos_incident import SOSIncident

class IncidentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_uuid(self, incident_uuid: str) -> Optional[SOSIncident]:
        stmt = select(SOSIncident).options(
            selectinload(SOSIncident.breadcrumbs),
            selectinload(SOSIncident.user)
        ).where(SOSIncident.incident_uuid == incident_uuid)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_active_user_incident(self, user_id: int) -> Optional[SOSIncident]:
        stmt = select(SOSIncident).where(
            SOSIncident.user_id == user_id,
            SOSIncident.status == "ACTIVE"
        ).order_by(SOSIncident.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_user_incidents(self, user_id: int, limit: int = 20) -> List[SOSIncident]:
        stmt = select(SOSIncident).where(SOSIncident.user_id == user_id).order_by(SOSIncident.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, incident: SOSIncident) -> SOSIncident:
        self.db.add(incident)
        await self.db.commit()
        await self.db.refresh(incident)
        return incident

    async def update(self, incident: SOSIncident) -> SOSIncident:
        await self.db.commit()
        await self.db.refresh(incident)
        return incident
