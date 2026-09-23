[app]

# (str) Title of your application
title = AlertX

# (str) Package name
package.name = alertx2

# (str) Package domain (needed for android/ios packaging)
package.domain = com.alertx

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (use # to filter)
source.include_exts = py,png,jpg,kv,atlas,json,md,txt

# (str) Application versioning (method 1)
version = 2.0.0

# (list) Application requirements
# Comma separated list of python packages
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pyjnius,plyer,requests,urllib3,certifi,charset-normalizer,idna,cryptography,bcrypt,aiohttp

# (str) Custom source folders for requirements
# requirements.source.kivymd = ../../kivymd

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/assets/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/assets/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,SEND_SMS,CALL_PHONE,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,CAMERA,RECEIVE_BOOT_COMPLETED,FOREGROUND_SERVICE,VIBRATE,ACCESS_BACKGROUND_LOCATION,READ_CONTACTS

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK / AAB will support.
android.minapi = 24

# (int) Android SDK version to use
android.sdk = 34

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to run after a network error on the android.sdk download
# android.skip_update = False

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
android.wakelock = False

# (list) Android application meta-data to set (key=value format)
android.meta_data =

# (list) Android library project to add (will be added in the
# temporary directory)
# android.library_references =

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Android allow backup feature (Android API >= 23)
android.allow_backup = True

# (str) Format used to package the application: apk or aar or aab
android.release_artifact = apk

# (str) Format used to package the application in debug mode: apk or aar or aab
android.debug_artifact = apk

# (list) Gradle dependencies to add
android.gradle_dependencies =

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains an 'androidx' package, or @android.usesdeprecated
android.enable_androidx = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# bin_dir = ./bin
