from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.tracking_service import TrackingService

router = APIRouter()

@router.get("/{incident_uuid}")
async def get_tracking_data(incident_uuid: str, db: AsyncSession = Depends(get_db)):
    tracking_service = TrackingService(db)
    data = await tracking_service.get_live_tracking_data(incident_uuid)
    if not data:
        raise HTTPException(status_code=404, detail="Tracking incident not found")
    return data
