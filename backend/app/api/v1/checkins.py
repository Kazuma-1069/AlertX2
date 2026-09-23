from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.checkin import CheckInCreate, CheckInResponse
from app.services.safety_service import SafetyService

router = APIRouter()

@router.post("", response_model=CheckInResponse)
async def submit_checkin(checkin_in: CheckInCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = SafetyService(db)
    return await service.record_checkin(
        user_id=current_user.id,
        message=checkin_in.status_message,
        lat=checkin_in.latitude,
        lng=checkin_in.longitude,
        address=checkin_in.address
    )
