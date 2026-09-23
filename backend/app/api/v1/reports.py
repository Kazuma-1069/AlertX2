from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.report import CommunityReportCreate, CommunityReportResponse
from app.services.report_service import ReportService

router = APIRouter()

@router.post("", response_model=CommunityReportResponse)
async def submit_report(
    report_in: CommunityReportCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ReportService(db)
    return await service.submit_report(
        user_id=current_user.id,
        report_type=report_in.type,
        description=report_in.description,
        lat=report_in.latitude,
        lng=report_in.longitude,
        media_reference=report_in.media_reference,
    )

@router.get("", response_model=List[CommunityReportResponse])
async def list_user_reports(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ReportService(db)
    return await service.get_user_reports(current_user.id)
