from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class MedicalProfile(Base):
    __tablename__ = "medical_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    blood_group = Column(String(10), nullable=True)  # A+, B+, O+, AB+, O-, etc.
    allergies = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    medical_information = Column(Text, nullable=True)
    physician_name = Column(String(255), nullable=True)
    physician_phone = Column(String(50), nullable=True)
    is_shared_with_responders = Column(Boolean, default=False, nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="medical_profile")
