#!/usr/bin/env bash
set -e

echo "Compiling AlertX2 Android APK via Buildozer..."
cd android
buildozer -v android debug
echo "Build completed. Check android/bin/ for the generated APK."
