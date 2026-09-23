from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class TrackingSession(Base):
    __tablename__ = "tracking_sessions"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("sos_incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    secure_token = Column(String(64), unique=True, index=True, nullable=False)  # Opaque URL-safe token
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    ended_at = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True, nullable=False)

    incident = relationship("SOSIncident", back_populates="tracking_sessions")
