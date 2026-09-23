from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AlertX2"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    SECRET_KEY: str = "super-secret-alertx2-signing-key-for-development-32b"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    DATABASE_URL: str = "sqlite+aiosqlite:///./alertx2.db"
    
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # Twilio / Telephony
    TWILIO_ACCOUNT_SID: str = "mock_sid"
    TWILIO_AUTH_TOKEN: str = "mock_token"
    TWILIO_PHONE_NUMBER: str = "+1234567890"
    TWILIO_WHATSAPP_NUMBER: str = "whatsapp:+14155238886"

    # Geolocation / Maps
    GOOGLE_MAPS_API_KEY: str = "mock_maps_key"

    # AI Guidance
    AI_API_KEY: str = "mock_ai_key"
    AI_MODEL_NAME: str = "gemini-1.5-flash"

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

settings = Settings()
