from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.guide import SafetyGuideResponse
from app.services.guide_service import GuideService

router = APIRouter()

@router.get("", response_model=List[SafetyGuideResponse])
async def list_guides(category: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    service = GuideService(db)
    await service.seed_default_guides()
    return await service.list_guides(category)
