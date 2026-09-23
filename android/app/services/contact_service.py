from app.services.api_client import api_client

class ContactService:
    def get_contacts(self):
        return api_client.get("/api/v1/contacts")

    def add_contact(self, name, phone, relationship="Friend", is_primary=False):
        return api_client.post("/api/v1/contacts", {
            "name": name,
            "phone_number": phone,
            "relationship": relationship,
            "is_primary": is_primary
        })

contact_service = ContactService()
