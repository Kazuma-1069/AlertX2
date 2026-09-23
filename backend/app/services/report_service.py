from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.report import IncidentReport
from app.repositories.report_repository import ReportRepository

class ReportService:
    def __init__(self, db: AsyncSession):
        self.repo = ReportRepository(db)

    async def submit_report(self, user_id: int, report_type: str, title: str, description: str, lat: float = None, lng: float = None, address: str = None, is_anon: str = "NO") -> IncidentReport:
        report = IncidentReport(
            user_id=user_id,
            incident_type=report_type,
            title=title,
            description=description,
            latitude=lat,
            longitude=lng,
            address=address,
            is_anonymous=is_anon
        )
        return await self.repo.create(report)

    async def get_user_reports(self, user_id: int) -> List[IncidentReport]:
        return await self.repo.get_by_user(user_id)
