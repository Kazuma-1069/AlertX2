from app.utils.logger import app_logger

class NativeSMSManager:
    def send_direct_sms(self, phone_number: str, message: str):
        app_logger.info(f"Sending direct SMS to {phone_number}")
        try:
            from plyer import sms
            sms.send(recipient=phone_number, message=message)
        except Exception as e:
            app_logger.warning(f"Desktop/Fallback: Simulated SMS to {phone_number}: {e}")

native_sms = NativeSMSManager()
