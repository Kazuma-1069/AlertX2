from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.sos import SOSTriggerRequest, SOSResolveRequest, SOSIncidentResponse
from app.services.sos_service import SOSService

router = APIRouter()

@router.post("/trigger", response_model=SOSIncidentResponse)
async def trigger_sos(req: SOSTriggerRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    sos_service = SOSService(db)
    incident = await sos_service.trigger_sos(
        user_id=current_user.id,
        user_name=current_user.full_name,
        lat=req.latitude,
        lng=req.longitude,
        address=req.address,
        trigger_type=req.trigger_type,
        battery=req.battery_level
    )
    return incident

@router.post("/resolve", response_model=SOSIncidentResponse)
async def resolve_sos(req: SOSResolveRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    sos_service = SOSService(db)
    incident = await sos_service.resolve_sos(req.incident_uuid, req.resolution_notes, req.status)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident
