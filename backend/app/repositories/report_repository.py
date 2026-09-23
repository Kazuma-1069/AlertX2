from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.report import CommunityReport


class ReportRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, report: CommunityReport) -> CommunityReport:
        self.db.add(report)
        await self.db.commit()
        await self.db.refresh(report)
        return report

    async def get_by_user(self, user_id: int) -> List[CommunityReport]:
        stmt = (
            select(CommunityReport)
            .where(CommunityReport.user_id == user_id)
            .order_by(CommunityReport.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
