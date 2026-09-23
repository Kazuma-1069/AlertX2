"""Direct Emergency SMS Dispatch via Android SmsManager."""
from app.utils.logger import app_logger
from app.utils.storage import local_store

class NativeSMSManager:
    def broadcast_emergency_sms(self, message: str):
        contacts = local_store.get("emergency_contacts", [])
        for contact in contacts:
            if contact.get("receive_sos", True):
                self.send_sms(contact.get("phone", ""), message)

    def send_sms(self, phone: str, message: str):
        if not phone:
            return
        app_logger.info(f"Sending emergency SMS to {phone}: {message[:60]}...")
        try:
            from jnius import autoclass
            SmsManager = autoclass('android.telephony.SmsManager')
            sms = SmsManager.getDefault()
            sms.sendTextMessage(phone, None, message, None, None)
            app_logger.info(f"Android SmsManager dispatched SMS to {phone}")
        except Exception:
            try:
                from plyer import sms
                sms.send(recipient=phone, message=message)
            except Exception:
                app_logger.info(f"[Desktop/Simulation] Emergency SMS sent to {phone}: {message}")

native_sms = NativeSMSManager()
