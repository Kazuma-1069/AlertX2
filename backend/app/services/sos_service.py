import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sos_incident import SOSIncident
from app.models.location import LocationBreadcrumb
from app.repositories.incident_repository import IncidentRepository
from app.repositories.contact_repository import ContactRepository
from app.services.notification_service import notification_service

class SOSService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.incident_repo = IncidentRepository(db)
        self.contact_repo = ContactRepository(db)

    async def trigger_sos(self, user_id: int, user_name: str, lat: float, lng: float, address: Optional[str] = None, trigger_type: str = "MANUAL_BUTTON", battery: Optional[int] = None) -> SOSIncident:
        incident_uuid = str(uuid.uuid4())
        incident = SOSIncident(
            incident_uuid=incident_uuid,
            user_id=user_id,
            trigger_type=trigger_type,
            status="ACTIVE",
            initial_latitude=lat,
            initial_longitude=lng,
            initial_address=address or f"Lat: {lat:.5f}, Lng: {lng:.5f}",
            battery_level=battery,
            created_at=datetime.now(timezone.utc)
        )
        saved_incident = await self.incident_repo.create(incident)

        # Record initial breadcrumb
        breadcrumb = LocationBreadcrumb(
            incident_id=saved_incident.id,
            latitude=lat,
            longitude=lng,
            battery_level=battery
        )
        self.db.add(breadcrumb)
        await self.db.commit()

        # Broadcast alerts to emergency contacts
        contacts = await self.contact_repo.get_user_contacts(user_id)
        if contacts:
            await notification_service.broadcast_sos(user_name, contacts, lat, lng, incident_uuid)

        return saved_incident

    async def resolve_sos(self, incident_uuid: str, notes: str = "Resolved by user", status: str = "RESOLVED") -> Optional[SOSIncident]:
        incident = await self.incident_repo.get_by_uuid(incident_uuid)
        if not incident:
            return None
        incident.status = status
        incident.resolved_at = datetime.now(timezone.utc)
        incident.resolution_notes = notes
        return await self.incident_repo.update(incident)
