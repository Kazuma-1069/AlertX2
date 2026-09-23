from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship as orm_relationship
from app.core.database import Base

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    relationship = Column(String(100), default="Friend")
    priority = Column(Integer, default=1, nullable=False, index=True)  # Priority 1 -> Contact A, Priority 2 -> Contact B
    receive_sos = Column(Boolean, default=True, nullable=False)
    receive_location = Column(Boolean, default=True, nullable=False)
    receive_checkin_alert = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = orm_relationship("User", back_populates="emergency_contacts")

# Backward compatibility alias
Contact = EmergencyContact
