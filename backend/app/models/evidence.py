from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Evidence(Base):
    __tablename__ = "evidences"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("sos_incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(String(50), nullable=False)  # AUDIO, IMAGE, SENSOR
    storage_reference = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    upload_status = Column(String(50), default="PENDING", nullable=False)  # PENDING, UPLOADED, FAILED

    incident = relationship("SOSIncident", back_populates="evidences")
