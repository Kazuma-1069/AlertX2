# Android Native Integration Guide

AlertX2 utilizes Android native capabilities via Python's `jnius` and `plyer` abstractions:

## Required Android Permissions

- `ACCESS_FINE_LOCATION`: Required for GPS latitude and longitude breadcrumbs.
- `ACCESS_COARSE_LOCATION`: Fallback network cell tower / Wi-Fi trilateration.
- `SEND_SMS`: Required to send hardware-level SMS emergency messages even when mobile data is down.
- `CALL_PHONE`: Allows one-touch dialing to emergency hotlines (e.g. 112 / 911).
- `RECORD_AUDIO`: Activates ambient mic capture during active SOS for forensic evidence.
- `FOREGROUND_SERVICE`: Prevents Android OS from killing location tracking while the screen is locked.

## Buildozer Packaging

The application is built into an APK using Buildozer:
```bash
buildozer android debug
```
