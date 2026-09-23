from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.tracking_repository import TrackingRepository

class TrackingService:
    def __init__(self, db: AsyncSession):
        self.repo = TrackingRepository(db)

    async def get_public_tracking_view(self, secure_token: str) -> Optional[Dict[str, Any]]:
        session = await self.repo.get_by_token(secure_token)
        if not session or not session.incident:
            return None
        
        incident = session.incident
        # Public data view: intentionally strips user_id, private notes, and internal DB keys
        return {
            "secure_token": session.secure_token,
            "status": incident.status,
            "active": session.active and incident.status == "ACTIVE",
            "started_at": incident.started_at.isoformat(),
            "last_latitude": incident.last_latitude,
            "last_longitude": incident.last_longitude,
            "location_accuracy": incident.location_accuracy,
            "breadcrumbs": [
                {
                    "latitude": b.latitude,
                    "longitude": b.longitude,
                    "accuracy": b.accuracy,
                    "timestamp": b.timestamp.isoformat()
                }
                for b in (incident.breadcrumbs or [])
            ],
            "timeline": [
                {
                    "event_type": e.event_type,
                    "timestamp": e.timestamp.isoformat()
                }
                for e in (incident.events or [])
            ]
        }
