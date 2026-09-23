from app.core.config import settings
from app.core.logging import logger

class WhatsAppService:
    async def send_whatsapp(self, to_phone: str, message: str) -> dict:
        logger.info(f"[WhatsApp Gateway] Sending WhatsApp message to {to_phone}")
        return {
            "status": "SENT",
            "provider": "TWILIO_WHATSAPP",
            "to": to_phone,
            "message_id": f"wa_mock_{to_phone[-4:]}"
        }

whatsapp_service = WhatsAppService()
