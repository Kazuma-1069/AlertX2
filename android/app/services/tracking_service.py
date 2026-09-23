from app.services.api_client import api_client

class TrackingService:
    def fetch_tracking(self, incident_uuid):
        return api_client.get(f"/api/v1/tracking/{incident_uuid}")

tracking_service = TrackingService()
