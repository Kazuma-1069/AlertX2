from typing import List
from app.models.contact import Contact
from app.services.sms_service import sms_service
from app.services.whatsapp_service import whatsapp_service
from app.services.call_service import call_service
from app.core.logging import logger

class NotificationService:
    async def broadcast_sos(self, user_name: str, contacts: List[Contact], lat: float, lng: float, incident_uuid: str) -> List[dict]:
        map_link = f"https://maps.google.com/?q={lat},{lng}"
        message = (
            f"EMERGENCY ALERT: {user_name} has triggered an SOS on AlertX2! "
            f"Current Location: {map_link} "
            f"Live Tracking: https://alertx2.app/track/{incident_uuid}"
        )
        results = []
        for contact in contacts:
            if contact.receive_sms:
                res = await sms_service.send_sms(contact.phone_number, message)
                results.append(res)
            if contact.receive_whatsapp:
                res = await whatsapp_service.send_whatsapp(contact.phone_number, message)
                results.append(res)
            if contact.receive_call:
                res = await call_service.place_emergency_call(contact.phone_number, f"Emergency alert from {user_name}")
                results.append(res)
        return results

notification_service = NotificationService()
