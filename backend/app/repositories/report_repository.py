from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.report import IncidentReport

class ReportRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, report: IncidentReport) -> IncidentReport:
        self.db.add(report)
        await self.db.commit()
        await self.db.refresh(report)
        return report

    async def get_by_user(self, user_id: int) -> List[IncidentReport]:
        stmt = select(IncidentReport).where(IncidentReport.user_id == user_id).order_by(IncidentReport.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
