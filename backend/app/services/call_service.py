from app.core.config import settings
from app.core.logging import logger

class CallService:
    async def place_emergency_call(self, to_phone: str, alert_message: str) -> dict:
        logger.info(f"[Voice Gateway] Placing automated emergency IVR call to {to_phone}")
        return {
            "status": "INITIATED",
            "provider": "TWILIO_VOICE",
            "call_sid": f"call_mock_{to_phone[-4:]}",
            "recipient": to_phone
        }

call_service = CallService()
