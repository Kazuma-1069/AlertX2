from app.native.android_recording import native_recording

class RecordingService:
    def start_emergency_recording(self):
        native_recording.start_recording("incident_audio.mp4")

    def stop_emergency_recording(self):
        native_recording.stop_recording()

recording_service = RecordingService()
