from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, MedicalProfileCreate, MedicalProfileResponse, UserSettingsUpdate, UserSettingsResponse
from app.models.medical_profile import MedicalProfile
from app.models.user_settings import UserSettings
from sqlalchemy.future import select

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_profile(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.phone_number is not None:
        current_user.phone_number = user_update.phone_number
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.post("/me/medical", response_model=MedicalProfileResponse)
async def upsert_medical_profile(profile_in: MedicalProfileCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    stmt = select(MedicalProfile).where(MedicalProfile.user_id == current_user.id)
    res = await db.execute(stmt)
    profile = res.scalars().first()
    if not profile:
        profile = MedicalProfile(user_id=current_user.id)
        db.add(profile)
    for field, val in profile_in.model_dump(exclude_unset=True).items():
        setattr(profile, field, val)
    await db.commit()
    await db.refresh(profile)
    return profile

@router.put("/me/settings", response_model=UserSettingsResponse)
async def update_settings(settings_in: UserSettingsUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    stmt = select(UserSettings).where(UserSettings.user_id == current_user.id)
    res = await db.execute(stmt)
    settings = res.scalars().first()
    if not settings:
        settings = UserSettings(user_id=current_user.id)
        db.add(settings)
    for field, val in settings_in.model_dump(exclude_unset=True).items():
        setattr(settings, field, val)
    await db.commit()
    await db.refresh(settings)
    return settings
