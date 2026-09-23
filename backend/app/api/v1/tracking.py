from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.tracking_service import TrackingService

router = APIRouter()

@router.get("/{secure_token}")
async def get_public_tracking(secure_token: str, db: AsyncSession = Depends(get_db)):
    service = TrackingService(db)
    view = await service.get_public_tracking_view(secure_token)
    if not view:
        raise HTTPException(status_code=404, detail="Tracking session not found or expired")
    return view
