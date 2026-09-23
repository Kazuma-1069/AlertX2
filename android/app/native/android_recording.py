from app.utils.logger import app_logger

class NativeAudioRecorder:
    def start_recording(self, output_path: str):
        app_logger.info(f"Recording incident ambient audio -> {output_path}")

    def stop_recording(self):
        app_logger.info("Audio recording stopped.")

native_recording = NativeAudioRecorder()
