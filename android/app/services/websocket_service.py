from app.utils.logger import app_logger

class WebSocketService:
    def connect_incident_stream(self, incident_uuid):
        app_logger.info(f"Connecting to live WebSocket stream for {incident_uuid}")

websocket_service = WebSocketService()
