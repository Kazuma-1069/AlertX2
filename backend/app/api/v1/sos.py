from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.sos import SOSTriggerRequest, SOSResolveRequest, SOSIncidentResponse
from app.services.sos_service import SOSService
from app.repositories.incident_repository import IncidentRepository

router = APIRouter()

@router.post("", response_model=SOSIncidentResponse)
async def trigger_sos(
    req: SOSTriggerRequest, 
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db),
    idempotency_key: Optional[str] = Header(None)
):
    service = SOSService(db)
    incident = await service.trigger_sos(
        user_id=current_user.id,
        user_name=current_user.name,
        lat=req.latitude,
        lng=req.longitude,
        accuracy=req.accuracy,
        activation_method=req.activation_method,
        idempotency_key=req.idempotency_key or idempotency_key
    )
    
    token = incident.tracking_sessions[0].secure_token if incident.tracking_sessions else None
    resp = SOSIncidentResponse(
        id=incident.id,
        user_id=incident.user_id,
        status=incident.status,
        activation_method=incident.activation_method,
        started_at=incident.started_at,
        resolved_at=incident.resolved_at,
        cancelled_at=incident.cancelled_at,
        last_latitude=incident.last_latitude,
        last_longitude=incident.last_longitude,
        location_accuracy=incident.location_accuracy,
        secure_tracking_token=token,
        events=incident.events
    )
    return resp

@router.get("/active", response_model=Optional[SOSIncidentResponse])
async def get_active_incident(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = IncidentRepository(db)
    incident = await repo.get_active_incident(current_user.id)
    if not incident:
        return None
    token = incident.tracking_sessions[0].secure_token if incident.tracking_sessions else None
    return SOSIncidentResponse(
        id=incident.id,
        user_id=incident.user_id,
        status=incident.status,
        activation_method=incident.activation_method,
        started_at=incident.started_at,
        resolved_at=incident.resolved_at,
        cancelled_at=incident.cancelled_at,
        last_latitude=incident.last_latitude,
        last_longitude=incident.last_longitude,
        location_accuracy=incident.location_accuracy,
        secure_tracking_token=token,
        events=incident.events
    )

@router.post("/resolve", response_model=SOSIncidentResponse)
async def resolve_sos(req: SOSResolveRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = SOSService(db)
    incident = await service.resolve_sos(req.incident_id, current_user.id, req.resolution_notes, req.status)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found or unauthorized")
    token = incident.tracking_sessions[0].secure_token if incident.tracking_sessions else None
    return SOSIncidentResponse(
        id=incident.id,
        user_id=incident.user_id,
        status=incident.status,
        activation_method=incident.activation_method,
        started_at=incident.started_at,
        resolved_at=incident.resolved_at,
        cancelled_at=incident.cancelled_at,
        last_latitude=incident.last_latitude,
        last_longitude=incident.last_longitude,
        location_accuracy=incident.location_accuracy,
        secure_tracking_token=token,
        events=incident.events
    )
