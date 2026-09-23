# Android background foreground service hook
import time
from app.utils.logger import app_logger

def run_service():
    app_logger.info("AlertX2 background service started...")
    while True:
        time.sleep(15)

if __name__ == "__main__":
    run_service()
