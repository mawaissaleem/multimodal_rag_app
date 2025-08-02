import os
import uuid
import logging
import ffmpeg
from pydub import AudioSegment
from backend.services.whisper.transcriber import WhisperTranscriber

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoIngestor:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.audio_path = f"/tmp/{uuid.uuid4()}.mp3"
        self.transcriber = WhisperTranscriber()
        self.cleaned_up = False

    def extract_audio(self):
        try:
            logger.info(f"Extracting audio from {self.video_path}")
            # Use ffmpeg-python to extract audio
            stream = ffmpeg.input(self.video_path)
            stream = ffmpeg.output(
                stream, self.audio_path, acodec="mp3", loglevel="quiet"
            )
            ffmpeg.run(stream)

            # Verify audio file exists
            if not os.path.exists(self.audio_path):
                raise ValueError("No audio stream found in the video.")

            # Load with pydub to ensure it's valid
            audio = AudioSegment.from_file(self.audio_path, format="mp3")
            logger.info(f"Audio extracted to {self.audio_path}")
        except Exception as e:
            logger.error(f"Error extracting audio: {e}")
            raise

    def transcribe_audio(self):
        try:
            logger.info(f"Transcribing audio from {self.audio_path}")
            segments = self.transcriber.transcribe(self.audio_path)
            logger.info(f"Transcription complete with {len(segments)} segments.")
            return segments
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            raise

    def ingest(self):
        self.extract_audio()
        segments = self.transcribe_audio()
        return {"transcript": segments}

    def cleanup(self):
        if not self.cleaned_up and os.path.exists(self.audio_path):
            os.remove(self.audio_path)
            logger.info(f"Cleaned up temporary audio file: {self.audio_path}")
            self.cleaned_up = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cleanup()

    def __del__(self):
        self.cleanup()
