from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.contact import Contact

class ContactRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_contacts(self, user_id: int) -> List[Contact]:
        stmt = select(Contact).where(Contact.user_id == user_id).order_by(Contact.is_primary.desc(), Contact.id.asc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, contact_id: int, user_id: int) -> Optional[Contact]:
        stmt = select(Contact).where(Contact.id == contact_id, Contact.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, contact: Contact) -> Contact:
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def delete(self, contact: Contact) -> None:
        await self.db.delete(contact)
        await self.db.commit()
