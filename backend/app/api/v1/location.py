from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.location import LocationBreadcrumbCreate, LocationBreadcrumbResponse
from app.services.location_service import LocationService

router = APIRouter()

@router.post("/breadcrumb", response_model=LocationBreadcrumbResponse)
async def record_breadcrumb(data: LocationBreadcrumbCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    loc_service = LocationService(db)
    crumb = await loc_service.record_breadcrumb(
        incident_uuid=data.incident_uuid,
        lat=data.latitude,
        lng=data.longitude,
        accuracy=data.accuracy,
        speed=data.speed,
        altitude=data.altitude,
        battery=data.battery_level
    )
    if not crumb:
        raise HTTPException(status_code=404, detail="Incident not found for telemetry breadcrumb")
    return crumb
