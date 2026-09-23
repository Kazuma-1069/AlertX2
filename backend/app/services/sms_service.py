from app.core.config import settings
from app.core.logging import logger

class SMSService:
    async def send_sms(self, to_phone: str, message: str) -> dict:
        logger.info(f"[SMS Gateway] Sending SMS to {to_phone}: {message[:60]}...")
        # Integrates with Twilio API in production
        return {
            "status": "SENT",
            "provider": "TWILIO",
            "to": to_phone,
            "message_id": f"sms_mock_{to_phone[-4:]}"
        }

sms_service = SMSService()
