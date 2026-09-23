from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, Text
from app.core.database import Base

class SafetyGuide(Base):
    __tablename__ = "safety_guides"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), index=True, nullable=False)  # Medical, Natural Disaster, Assault, Fire, Traffic
    title = Column(String(255), nullable=False)
    summary = Column(String(500), nullable=False)
    steps_json = Column(Text, nullable=False)  # JSON serialized steps list
    dos_and_donts_json = Column(Text, nullable=True)
    emergency_numbers_json = Column(Text, nullable=True)
    icon_name = Column(String(100), default="shield-alert")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
