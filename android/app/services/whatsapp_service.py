from app.utils.logger import app_logger

class WhatsAppService:
    def send_whatsapp(self, phone, message):
        app_logger.info(f"Direct WhatsApp link generated for {phone}: {message[:40]}...")

whatsapp_service = WhatsAppService()
