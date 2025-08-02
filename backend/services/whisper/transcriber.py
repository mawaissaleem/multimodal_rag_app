from faster_whisper import WhisperModel
from typing import List, Dict


class WhisperTranscriber:
    def __init__(self, model_size: str = "tiny"):
        # You can change to "tiny" for even lower memory usage
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def transcribe(self, audio_path: str) -> List[Dict[str, str]]:
        segments, _ = self.model.transcribe(audio_path)
        output = []
        for segment in segments:
            output.append(
                {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip(),
                }
            )
        return output
