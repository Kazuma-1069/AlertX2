from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class SOSIncident(Base):
    __tablename__ = "sos_incidents"

    id = Column(Integer, primary_key=True, index=True)
    incident_uuid = Column(String(36), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    trigger_type = Column(String(50), default="MANUAL_BUTTON")  # MANUAL_BUTTON, HARDWARE_KEY, TIMER_EXPIRY, FALL_DETECTED
    status = Column(String(50), default="ACTIVE", index=True)  # ACTIVE, RESOLVED, CANCELLED, FALSE_ALARM
    initial_latitude = Column(Float, nullable=False)
    initial_longitude = Column(Float, nullable=False)
    initial_address = Column(String(500), nullable=True)
    battery_level = Column(Integer, nullable=True)
    network_status = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="incidents")
    breadcrumbs = relationship("LocationBreadcrumb", back_populates="incident", cascade="all, delete-orphan")
    evidences = relationship("IncidentEvidence", back_populates="incident", cascade="all, delete-orphan")
    notifications = relationship("NotificationLog", back_populates="incident", cascade="all, delete-orphan")
    calls = relationship("CallLog", back_populates="incident", cascade="all, delete-orphan")
