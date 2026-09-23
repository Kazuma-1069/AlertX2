from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class SafetyTimer(Base):
    __tablename__ = "safety_timers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    duration = Column(Integer, nullable=False)  # Duration in minutes: 5, 15, 30, 60, custom
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    status = Column(String(50), default="ACTIVE", index=True, nullable=False)  # ACTIVE, COMPLETED, EXPIRED, CANCELLED
    title = Column(String(255), default="Walking Alone")
    destination = Column(String(255), nullable=True)

    user = relationship("User", back_populates="safety_timers")
