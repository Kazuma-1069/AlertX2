from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.contact import EmergencyContact

class ContactRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_contacts(self, user_id: int) -> List[EmergencyContact]:
        stmt = select(EmergencyContact).where(EmergencyContact.user_id == user_id).order_by(EmergencyContact.priority.asc(), EmergencyContact.id.asc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, contact_id: int, user_id: int) -> Optional[EmergencyContact]:
        stmt = select(EmergencyContact).where(EmergencyContact.id == contact_id, EmergencyContact.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, contact: EmergencyContact) -> EmergencyContact:
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def update(self, contact: EmergencyContact) -> EmergencyContact:
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def delete(self, contact: EmergencyContact) -> None:
        await self.db.delete(contact)
        await self.db.commit()
