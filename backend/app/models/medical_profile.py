from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class MedicalProfile(Base):
    __tablename__ = "medical_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    blood_group = Column(String(10), nullable=True)  # e.g., A+, O-, etc.
    allergies = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    chronic_conditions = Column(Text, nullable=True)
    emergency_notes = Column(Text, nullable=True)
    physician_name = Column(String(255), nullable=True)
    physician_phone = Column(String(50), nullable=True)
    insurance_provider = Column(String(255), nullable=True)
    insurance_policy_number = Column(String(100), nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="medical_profile")
