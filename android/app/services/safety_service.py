from app.services.api_client import api_client

class SafetyService:
    def start_timer(self, title, duration_minutes, destination=None):
        return api_client.post("/api/v1/safety/timer", {
            "title": title,
            "duration_minutes": duration_minutes,
            "destination_name": destination
        })

safety_service = SafetyService()
