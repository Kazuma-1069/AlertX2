[app]
title = AlertX2
package.name = alertx2
package.domain = org.alertx
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 2.0.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests,urllib3,plyer,certifi,websocket-client

orientation = portrait
fullscreen = 0

# Android specific
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,SEND_SMS,CALL_PHONE,RECORD_AUDIO,WAKE_LOCK,FOREGROUND_SERVICE,VIBRATE,RECEIVE_BOOT_COMPLETED
android.api = 33
android.minapi = 26
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.service = AlertXService:app/native/android_service.py

[buildozer]
log_level = 2
warn_on_root = 1
