from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sos_incident import SOSIncident
from app.models.location import LocationBreadcrumb
from app.repositories.incident_repository import IncidentRepository
from app.repositories.contact_repository import ContactRepository
from app.services.notification_service import notification_service
from app.core.logging import logger

class SOSService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.incident_repo = IncidentRepository(db)
        self.contact_repo = ContactRepository(db)

    async def trigger_sos(
        self,
        user_id: int,
        user_name: str,
        lat: float,
        lng: float,
        accuracy: Optional[float] = None,
        activation_method: str = "BUTTON",
        idempotency_key: Optional[str] = None
    ) -> SOSIncident:
        # Idempotency check: prevent duplicate incidents caused by multiple clicks or retries
        if idempotency_key:
            existing = await self.incident_repo.get_by_idempotency_key(idempotency_key)
            if existing:
                logger.info(f"Duplicate SOS trigger suppressed via idempotency key: {idempotency_key}")
                return existing

        incident = SOSIncident(
            user_id=user_id,
            status="ACTIVE",
            activation_method=activation_method,
            started_at=datetime.now(timezone.utc),
            last_latitude=lat,
            last_longitude=lng,
            location_accuracy=accuracy,
            idempotency_key=idempotency_key
        )
        saved = await self.incident_repo.create(incident)

        # Store initial location breadcrumb
        breadcrumb = LocationBreadcrumb(
            incident_id=saved.id,
            latitude=lat,
            longitude=lng,
            accuracy=accuracy
        )
        self.db.add(breadcrumb)
        await self.db.commit()

        # Get tracking token
        tracking_token = saved.tracking_sessions[0].secure_token if saved.tracking_sessions else ""

        # Fetch priority-ordered emergency contacts
        contacts = await self.contact_repo.get_user_contacts(user_id)
        if contacts:
            await self.incident_repo.add_event(saved.id, "CONTACT_NOTIFIED", f'{{"count": {len(contacts)}}}')
            # Trigger notifications in background/task
            await notification_service.broadcast_sos(user_name, contacts, lat, lng, tracking_token)

        return saved

    async def resolve_sos(self, incident_id: int, user_id: int, notes: str = "Resolved by user", status: str = "RESOLVED") -> Optional[SOSIncident]:
        incident = await self.incident_repo.get_by_id(incident_id)
        if not incident or incident.user_id != user_id:
            return None
        
        now = datetime.now(timezone.utc)
        incident.status = status
        if status == "RESOLVED":
            incident.resolved_at = now
        elif status == "CANCELLED":
            incident.cancelled_at = now

        # Deactivate tracking sessions
        for session in incident.tracking_sessions:
            session.active = False
            session.ended_at = now

        await self.incident_repo.add_event(incident.id, f"SOS_{status}", f'{{"notes": "{notes}"}}')
        return await self.incident_repo.update(incident)
