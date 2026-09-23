from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.user import User
from app.models.medical_profile import MedicalProfile
from app.models.user_settings import UserSettings

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        stmt = select(User).options(
            selectinload(User.medical_profile),
            selectinload(User.settings)
        ).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).options(
            selectinload(User.medical_profile),
            selectinload(User.settings)
        ).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_phone(self, phone: str) -> Optional[User]:
        stmt = select(User).where(User.phone_number == phone)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        # Create default settings
        settings = UserSettings(user_id=user.id)
        self.db.add(settings)
        await self.db.commit()
        await self.db.refresh(user)
        return user
