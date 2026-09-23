from app.utils.logger import app_logger

class NotificationService:
    def show_alert(self, title, message):
        app_logger.info(f"NOTIFICATION [{title}]: {message}")

notification_service = NotificationService()
