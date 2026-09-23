from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.report import IncidentReportCreate, IncidentReportResponse
from app.services.report_service import ReportService

router = APIRouter()

@router.post("", response_model=IncidentReportResponse)
async def submit_report(report_in: IncidentReportCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = ReportService(db)
    return await service.submit_report(
        user_id=current_user.id,
        report_type=report_in.incident_type,
        title=report_in.title,
        description=report_in.description,
        lat=report_in.latitude,
        lng=report_in.longitude,
        address=report_in.address,
        is_anon=report_in.is_anonymous
    )

@router.get("", response_model=List[IncidentReportResponse])
async def list_user_reports(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = ReportService(db)
    return await service.get_user_reports(current_user.id)
