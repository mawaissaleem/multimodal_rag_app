import pytest
from unittest.mock import patch, MagicMock
from backend.services.ingestion.video_ingestor import VideoIngestor


@patch("backend.services.ingestion.video_ingestor.os.remove")
@patch("backend.services.ingestion.video_ingestor.AudioSegment.from_file")
@patch("backend.services.ingestion.video_ingestor.ffmpeg.run")
@patch("backend.services.ingestion.video_ingestor.ffmpeg.output")
@patch("backend.services.ingestion.video_ingestor.ffmpeg.input")
@patch("backend.services.ingestion.video_ingestor.os.path.exists", return_value=True)
@patch("backend.services.ingestion.video_ingestor.WhisperTranscriber")
def test_video_ingestor_ingest_success(
    mock_transcriber_class,
    mock_exists,
    mock_ffmpeg_input,
    mock_ffmpeg_output,
    mock_ffmpeg_run,
    mock_audio_from_file,
    mock_os_remove,
):
    # Mock ffmpeg input/output chain
    mock_ffmpeg_output.return_value = "ffmpeg_stream"
    mock_ffmpeg_input.return_value = "input_stream"

    # Mock audio segment validation
    mock_audio_from_file.return_value = MagicMock()

    # Mock transcription
    mock_transcriber = MagicMock()
    mock_segment = {"start": 0.0, "end": 1.0, "text": "Sample text"}
    mock_transcriber.transcribe.return_value = [mock_segment]
    mock_transcriber_class.return_value = mock_transcriber

    with VideoIngestor("fake_video.mp4") as ingestor:
        result = ingestor.ingest()

    assert "transcript" in result
    assert result["transcript"][0]["text"] == "Sample text"
    mock_os_remove.assert_called_once()
