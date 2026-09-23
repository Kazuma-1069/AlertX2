from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class SOSIncident(Base):
    __tablename__ = "sos_incidents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(50), default="ACTIVE", index=True, nullable=False)  # ACTIVE, RESOLVED, CANCELLED
    activation_method = Column(String(50), default="BUTTON", nullable=False)  # BUTTON, FIVE_TAP, TIMER_EXPIRY, FALL_DETECTED
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    resolved_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    last_latitude = Column(Float, nullable=False)
    last_longitude = Column(Float, nullable=False)
    location_accuracy = Column(Float, nullable=True)
    idempotency_key = Column(String(64), unique=True, index=True, nullable=True)

    user = relationship("User", back_populates="sos_incidents")
    tracking_sessions = relationship("TrackingSession", back_populates="incident", cascade="all, delete-orphan")
    events = relationship("IncidentEvent", back_populates="incident", cascade="all, delete-orphan", order_by="IncidentEvent.timestamp")
    evidences = relationship("Evidence", back_populates="incident", cascade="all, delete-orphan")
    breadcrumbs = relationship("LocationBreadcrumb", back_populates="incident", cascade="all, delete-orphan")
