from datetime import timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User
from app.schemas.auth import Token
from app.repositories.user_repository import UserRepository

class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def create_user_token(self, user: User) -> Token:
        access_token = create_access_token(subject=user.id)
        return Token(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            full_name=user.full_name,
            email=user.email
        )

    async def register_user(self, email: str, phone: str, full_name: str, password: str) -> User:
        hashed_password = get_password_hash(password)
        new_user = User(
            email=email,
            phone_number=phone,
            full_name=full_name,
            hashed_password=hashed_password,
            is_active=True,
            is_verified=True
        )
        return await self.repo.create(new_user)
