import secrets
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.sos_incident import SOSIncident
from app.models.tracking_session import TrackingSession
from app.models.incident_event import IncidentEvent

class IncidentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, incident_id: int) -> Optional[SOSIncident]:
        stmt = select(SOSIncident).options(
            selectinload(SOSIncident.tracking_sessions),
            selectinload(SOSIncident.events),
            selectinload(SOSIncident.breadcrumbs)
        ).where(SOSIncident.id == incident_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_idempotency_key(self, key: str) -> Optional[SOSIncident]:
        if not key:
            return None
        stmt = select(SOSIncident).options(
            selectinload(SOSIncident.tracking_sessions),
            selectinload(SOSIncident.events)
        ).where(SOSIncident.idempotency_key == key)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_active_incident(self, user_id: int) -> Optional[SOSIncident]:
        stmt = select(SOSIncident).options(
            selectinload(SOSIncident.tracking_sessions),
            selectinload(SOSIncident.events)
        ).where(
            SOSIncident.user_id == user_id,
            SOSIncident.status == "ACTIVE"
        ).order_by(SOSIncident.started_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_user_history(self, user_id: int, limit: int = 20) -> List[SOSIncident]:
        stmt = select(SOSIncident).options(
            selectinload(SOSIncident.events)
        ).where(SOSIncident.user_id == user_id).order_by(SOSIncident.started_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, incident: SOSIncident) -> SOSIncident:
        self.db.add(incident)
        await self.db.flush()
        
        # Create initial TrackingSession with secure opaque token
        secure_token = secrets.token_urlsafe(32)
        tracking_session = TrackingSession(
            incident_id=incident.id,
            secure_token=secure_token,
            active=True
        )
        self.db.add(tracking_session)

        # Log initial event
        event = IncidentEvent(
            incident_id=incident.id,
            event_type="SOS_ACTIVATED",
            metadata_json=f'{{"method": "{incident.activation_method}"}}'
        )
        self.db.add(event)

        await self.db.commit()
        await self.db.refresh(incident)
        return incident

    async def add_event(self, incident_id: int, event_type: str, metadata: str = None) -> IncidentEvent:
        event = IncidentEvent(
            incident_id=incident_id,
            event_type=event_type,
            metadata_json=metadata
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def update(self, incident: SOSIncident) -> SOSIncident:
        await self.db.commit()
        await self.db.refresh(incident)
        return incident
