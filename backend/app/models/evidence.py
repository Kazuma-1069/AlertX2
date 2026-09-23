from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class IncidentEvidence(Base):
    __tablename__ = "incident_evidences"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("sos_incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    file_type = Column(String(50), nullable=False)  # AUDIO, IMAGE, VIDEO, SENSOR_LOG
    file_path = Column(String(500), nullable=False)
    checksum = Column(String(64), nullable=True)
    file_size_bytes = Column(Integer, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    incident = relationship("SOSIncident", back_populates="evidences")
