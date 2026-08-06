import json
from pathlib import Path
from typing import Any, Dict

from adapters.stt.base import BaseSTTAdapter


class MockSTTAdapter(BaseSTTAdapter):
    """Mock STT Adapter replaying exact ground-truth audio transcripts matching testdata/audio/."""

    def __init__(self, fixture_path: Path = None) -> None:
        if fixture_path is None:
            self.fixture_path = (
                Path(__file__).parent.parent.parent
                / "testdata"
                / "fixtures"
                / "sample_transcription.json"
            )
        else:
            self.fixture_path = fixture_path

    def transcribe(
        self, audio_bytes: bytes, filename: str, language: str
    ) -> Dict[str, Any]:
        fname = filename.lower()

        if "my-real-voice" in fname or "my_real_voice" in fname:
            return {
                "transcript": "hey so can you hear me and can you tell me what I am saying right now can you detect it actually or if you can tell me why you cannot",
                "language": "en" if language == "auto" else language,
                "duration_seconds": 9.38,
                "provider": "mock-stt",
            }
        elif "silence" in fname or "ambient" in fname:
            return {
                "transcript": "",
                "language": language if language and language != "auto" else "en",
                "duration_seconds": 3.0,
                "provider": "mock-stt",
            }
        elif "bn" in fname or "bengali" in fname or "golap" in fname:
            return {
                "transcript": "গোলাপ",
                "language": "bn" if language == "auto" else language,
                "duration_seconds": 1.2,
                "provider": "mock-stt",
            }
        elif "en" in fname or "doctor" in fname:
            return {
                "transcript": "doctor",
                "language": "en" if language == "auto" else language,
                "duration_seconds": 1.2,
                "provider": "mock-stt",
            }

        if not self.fixture_path.exists():
            return {
                "transcript": "doctor",
                "language": language if language and language != "auto" else "en",
                "duration_seconds": 1.2,
                "provider": "mock-stt",
            }

        data = json.loads(self.fixture_path.read_text(encoding="utf-8"))
        if language and language != "auto":
            data["language"] = language
        return data
