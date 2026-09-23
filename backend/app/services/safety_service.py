from datetime import datetime, timedelta, timezone
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.safety_timer import SafetyTimer
from app.models.checkin import CheckIn

class SafetyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def start_safety_timer(self, user_id: int, title: str, duration_minutes: int, destination: Optional[str] = None) -> SafetyTimer:
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=duration_minutes)
        timer = SafetyTimer(
            user_id=user_id,
            title=title,
            duration_minutes=duration_minutes,
            start_time=now,
            expires_at=expires_at,
            destination_name=destination,
            is_active=True
        )
        self.db.add(timer)
        await self.db.commit()
        await self.db.refresh(timer)
        return timer

    async def complete_safety_timer(self, timer_id: int, user_id: int) -> Optional[SafetyTimer]:
        stmt = select(SafetyTimer).where(SafetyTimer.id == timer_id, SafetyTimer.user_id == user_id)
        result = await self.db.execute(stmt)
        timer = result.scalars().first()
        if not timer:
            return None
        timer.is_active = False
        timer.is_completed = True
        await self.db.commit()
        await self.db.refresh(timer)
        return timer

    async def record_checkin(self, user_id: int, message: str, lat: Optional[float] = None, lng: Optional[float] = None, address: Optional[str] = None) -> CheckIn:
        checkin = CheckIn(
            user_id=user_id,
            status_message=message,
            latitude=lat,
            longitude=lng,
            address=address
        )
        self.db.add(checkin)
        await self.db.commit()
        await self.db.refresh(checkin)
        return checkin
