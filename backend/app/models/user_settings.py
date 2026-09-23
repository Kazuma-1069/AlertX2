from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    sos_countdown_seconds = Column(Integer, default=5, nullable=False)
    enable_fall_detection = Column(Boolean, default=False, nullable=False)
    enable_shake_trigger = Column(Boolean, default=True, nullable=False)
    power_button_trigger_count = Column(Integer, default=3, nullable=False)
    auto_record_audio_on_sos = Column(Boolean, default=True, nullable=False)
    share_battery_status = Column(Boolean, default=True, nullable=False)
    stealth_mode = Column(Boolean, default=False, nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="settings")
