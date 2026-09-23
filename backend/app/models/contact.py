from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(50), nullable=False)
    email = Column(String(255), nullable=True)
    relationship = Column(String(100), default="Friend")  # Family, Friend, Spouse, Doctor, etc.
    is_primary = Column(Boolean, default=False, nullable=False)
    receive_sms = Column(Boolean, default=True, nullable=False)
    receive_call = Column(Boolean, default=True, nullable=False)
    receive_whatsapp = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="contacts")
