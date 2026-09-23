from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.location import LocationBreadcrumb
from app.repositories.location_repository import LocationRepository
from app.repositories.incident_repository import IncidentRepository

class LocationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.loc_repo = LocationRepository(db)
        self.inc_repo = IncidentRepository(db)

    async def record_breadcrumb(self, incident_uuid: str, lat: float, lng: float, accuracy: Optional[float] = None, speed: Optional[float] = None, altitude: Optional[float] = None, battery: Optional[int] = None) -> Optional[LocationBreadcrumb]:
        incident = await self.inc_repo.get_by_uuid(incident_uuid)
        if not incident:
            return None
        breadcrumb = LocationBreadcrumb(
            incident_id=incident.id,
            latitude=lat,
            longitude=lng,
            accuracy=accuracy,
            speed=speed,
            altitude=altitude,
            battery_level=battery
        )
        return await self.loc_repo.add_breadcrumb(breadcrumb)
