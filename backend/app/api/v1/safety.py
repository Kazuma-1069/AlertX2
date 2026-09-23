from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.safety import SafetyTimerCreate, SafetyTimerCancelRequest, SafetyTimerResponse
from app.services.safety_service import SafetyService

router = APIRouter()

@router.post("/timer", response_model=SafetyTimerResponse)
async def create_timer(timer_in: SafetyTimerCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = SafetyService(db)
    return await service.start_safety_timer(
        user_id=current_user.id,
        title=timer_in.title,
        duration_minutes=timer_in.duration_minutes,
        destination=timer_in.destination_name
    )

@router.post("/timer/cancel", response_model=SafetyTimerResponse)
async def cancel_timer(req: SafetyTimerCancelRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = SafetyService(db)
    timer = await service.complete_safety_timer(req.timer_id, current_user.id)
    if not timer:
        raise HTTPException(status_code=404, detail="Safety timer not found")
    return timer
