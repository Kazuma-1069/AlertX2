from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.location import LocationBreadcrumb

class LocationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_breadcrumb(self, breadcrumb: LocationBreadcrumb) -> LocationBreadcrumb:
        self.db.add(breadcrumb)
        await self.db.commit()
        await self.db.refresh(breadcrumb)
        return breadcrumb

    async def get_incident_breadcrumbs(self, incident_id: int) -> List[LocationBreadcrumb]:
        stmt = select(LocationBreadcrumb).where(LocationBreadcrumb.incident_id == incident_id).order_by(LocationBreadcrumb.timestamp.asc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
