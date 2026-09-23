from app.utils.logger import app_logger

def request_android_permissions():
    try:
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.ACCESS_FINE_LOCATION,
            Permission.ACCESS_COARSE_LOCATION,
            Permission.SEND_SMS,
            Permission.CALL_PHONE,
            Permission.RECORD_AUDIO
        ])
        app_logger.info("Android permissions requested via JNI.")
    except ImportError:
        app_logger.info("Non-Android platform: Skipping native permission request.")
