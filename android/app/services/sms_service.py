from app.native.android_sms import native_sms

class SMSService:
    def send_sos_sms(self, phone, coords):
        msg = f"AlertX2 SOS ALERT! I need help. My current location is https://maps.google.com/?q={coords[0]},{coords[1]}"
        native_sms.send_direct_sms(phone, msg)

sms_service = SMSService()
