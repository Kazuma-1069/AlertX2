from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.sos import SOSIncidentResponse
from app.repositories.incident_repository import IncidentRepository

router = APIRouter()

@router.get("/history", response_model=List[SOSIncidentResponse])
async def get_incident_history(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = IncidentRepository(db)
    return await repo.get_user_incidents(current_user.id)
