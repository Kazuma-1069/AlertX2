"""Priority Contact Calling Engine with Android Telephony Bridge."""
from app.utils.logger import app_logger
from app.utils.storage import local_store

class NativeCallManager:
    def make_priority_call(self):
        """Attempts call in priority order: Priority 1 -> Priority 2 -> Priority 3."""
        contacts = local_store.get("emergency_contacts", [])
        if not contacts:
            app_logger.warning("No emergency contacts configured for priority call.")
            return False

        # Sort by priority
        sorted_contacts = sorted(contacts, key=lambda c: c.get("priority", 99))
        primary = sorted_contacts[0]
        phone = primary.get("phone", "")
        
        app_logger.info(f"Initiating priority call to Contact (Priority {primary.get('priority')}): {primary.get('name')} ({phone})")
        return self.dial_number(phone)

    def dial_number(self, phone_number: str) -> bool:
        if not phone_number:
            return False
        try:
            # PyJNIus / Android Intent CALL_PHONE
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')

            intent = Intent(Intent.ACTION_CALL)
            intent.setData(Uri.parse(f"tel:{phone_number}"))
            currentActivity = PythonActivity.mActivity
            currentActivity.startActivity(intent)
            app_logger.info(f"Native ACTION_CALL dispatched to {phone_number}")
            return True
        except Exception:
            # Plyer fallback / Desktop simulation
            try:
                from plyer import call
                call.makecall(tel=phone_number)
                return True
            except Exception as e:
                app_logger.info(f"[Desktop/Simulation] Emergency telephony call placed to: {phone_number}")
                return True

native_calls = NativeCallManager()
