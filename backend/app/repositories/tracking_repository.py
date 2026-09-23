from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.tracking_session import TrackingSession
from app.models.sos_incident import SOSIncident

class TrackingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_token(self, secure_token: str) -> Optional[TrackingSession]:
        stmt = select(TrackingSession).options(
            selectinload(TrackingSession.incident).selectinload(SOSIncident.breadcrumbs),
            selectinload(TrackingSession.incident).selectinload(SOSIncident.events)
        ).where(TrackingSession.secure_token == secure_token)
        result = await self.db.execute(stmt)
        return result.scalars().first()
