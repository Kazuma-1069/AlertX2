from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.report import CommunityReport
from app.repositories.report_repository import ReportRepository


class ReportService:
    def __init__(self, db: AsyncSession):
        self.repo = ReportRepository(db)

    async def submit_report(
        self,
        user_id: int,
        report_type: str,
        description: str,
        lat: float,
        lng: float,
        media_reference: Optional[str] = None,
    ) -> CommunityReport:
        report = CommunityReport(
            user_id=user_id,
            type=report_type,
            description=description,
            latitude=lat,
            longitude=lng,
            media_reference=media_reference,
            status="ACTIVE",
        )
        return await self.repo.create(report)

    async def get_user_reports(self, user_id: int) -> List[CommunityReport]:
        return await self.repo.get_by_user(user_id)
