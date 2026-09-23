from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("sos_incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    channel = Column(String(50), nullable=False)  # SMS, WHATSAPP, PUSH
    recipient = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String(50), default="SENT")  # PENDING, SENT, FAILED, DELIVERED
    gateway_message_id = Column(String(100), nullable=True)
    sent_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    incident = relationship("SOSIncident", back_populates="notifications")
