import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from backend.services.ingestion.video_ingestor import VideoIngestor

video_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../data/raw/video01.mp4")
)

with VideoIngestor(video_path) as ingestor:
    result = ingestor.ingest()

print("Transcription Segments:")
for segment in result["transcript"]:
    print(segment)
