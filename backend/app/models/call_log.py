from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class CallLog(Base):
    __tablename__ = "call_logs"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("sos_incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    recipient_phone = Column(String(50), nullable=False)
    status = Column(String(50), default="INITIATED")  # INITIATED, RINGING, ANSWERED, COMPLETED, FAILED
    call_sid = Column(String(100), nullable=True)
    duration_seconds = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    incident = relationship("SOSIncident", back_populates="calls")
