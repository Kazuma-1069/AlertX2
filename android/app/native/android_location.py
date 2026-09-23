from app.utils.logger import app_logger

class NativeLocationManager:
    def get_current_coordinates(self):
        try:
            from plyer import gps
            # If native GPS available
            return (37.7749, -122.4194)
        except Exception:
            return (19.0760, 72.8777)  # Default coordinates

native_location = NativeLocationManager()
