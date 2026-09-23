import json
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.guide import SafetyGuide

class GuideService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_guides(self, category: Optional[str] = None) -> List[SafetyGuide]:
        stmt = select(SafetyGuide)
        if category:
            stmt = stmt.where(SafetyGuide.category == category)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def seed_default_guides(self) -> None:
        stmt = select(SafetyGuide)
        res = await self.db.execute(stmt)
        if res.scalars().first() is None:
            guides = [
                SafetyGuide(
                    category="Medical",
                    title="CPR (Cardiopulmonary Resuscitation)",
                    summary="Hands-only CPR procedure for adults experiencing sudden cardiac arrest.",
                    steps_json=json.dumps([
                        "1. Verify scene safety and check for responsiveness.",
                        "2. Call emergency services (e.g. 911/112) or assign a bystander.",
                        "3. Place hands in the center of the chest.",
                        "4. Push hard and fast at 100-120 beats per minute (to the beat of Stayin' Alive).",
                        "5. Continue until emergency personnel take over or an AED arrives."
                    ]),
                    dos_and_donts_json=json.dumps({"dos": ["Push 2 inches deep", "Allow full chest recoil"], "donts": ["Do not stop compressions unnecessarily"]}),
                    emergency_numbers_json=json.dumps(["911", "112", "102"]),
                    icon_name="heart-pulse"
                ),
                SafetyGuide(
                    category="Natural Disaster",
                    title="Earthquake Survival (Drop, Cover, Hold On)",
                    summary="Immediate protective actions during a seismic tremor.",
                    steps_json=json.dumps([
                        "1. DROP down onto your hands and knees.",
                        "2. COVER your head and neck beneath a sturdy table or desk.",
                        "3. HOLD ON until shaking ceases.",
                        "4. Stay away from glass windows, exterior doors, and tall furniture.",
                        "5. If outside, move to a clear area away from power lines and buildings."
                    ]),
                    dos_and_donts_json=json.dumps({"dos": ["Protect your head and neck", "Stay indoors until shaking stops"], "donts": ["Do not use elevators"]}),
                    emergency_numbers_json=json.dumps(["911", "112", "108"]),
                    icon_name="earth"
                ),
                SafetyGuide(
                    category="Fire",
                    title="Structure Fire Evacuation",
                    summary="How to safely escape a smoke-filled building or residential fire.",
                    steps_json=json.dumps([
                        "1. Crawl low under smoke toward the nearest safe exit.",
                        "2. Feel closed door handles before opening; if hot, do not open.",
                        "3. Close doors behind you to slow the spread of flames and oxygen.",
                        "4. Once outside, remain at your designated meeting spot; never re-enter.",
                        "5. Call emergency dispatch immediately."
                    ]),
                    dos_and_donts_json=json.dumps({"dos": ["Stay low to avoid toxic smoke", "Test door temperatures"], "donts": ["Never go back inside for possessions"]}),
                    emergency_numbers_json=json.dumps(["911", "112", "101"]),
                    icon_name="fire"
                )
            ]
            self.db.add_all(guides)
            await self.db.commit()
