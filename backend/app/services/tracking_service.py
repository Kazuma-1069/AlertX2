from typing import Dict, Any, List
from app.repositories.incident_repository import IncidentRepository
from sqlalchemy.ext.asyncio import AsyncSession

class TrackingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = IncidentRepository(db)

    async def get_live_tracking_data(self, incident_uuid: str) -> Dict[str, Any]:
        incident = await self.repo.get_by_uuid(incident_uuid)
        if not incident:
            return {}
        return {
            "incident_uuid": incident.incident_uuid,
            "status": incident.status,
            "initial_location": {
                "latitude": incident.initial_latitude,
                "longitude": incident.initial_longitude,
                "address": incident.initial_address
            },
            "breadcrumbs": [
                {
                    "lat": b.latitude,
                    "lng": b.longitude,
                    "timestamp": b.timestamp.isoformat(),
                    "battery": b.battery_level
                }
                for b in (incident.breadcrumbs or [])
            ]
        }
