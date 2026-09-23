from app.utils.logger import app_logger

class NativeCallManager:
    def make_direct_call(self, phone_number: str):
        app_logger.info(f"Triggering direct mobile telephony call to {phone_number}")
        try:
            from plyer import call
            call.makecall(tel=phone_number)
        except Exception as e:
            app_logger.warning(f"Desktop/Fallback: Simulated phone call to {phone_number}: {e}")

native_calls = NativeCallManager()
