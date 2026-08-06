import json
from pathlib import Path
from typing import Any, Dict

from adapters.stt.base import BaseSTTAdapter


class MockSTTAdapter(BaseSTTAdapter):
    """Mock STT Adapter replaying disk fixtures with zero network calls or model downloads."""

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
        if not self.fixture_path.exists():
            raise FileNotFoundError(f"Mock STT fixture not found at {self.fixture_path}")

        data = json.loads(self.fixture_path.read_text(encoding="utf-8"))

        # Handle non-speech silence / ambient noise filenames gracefully
        if "silence" in filename.lower() or "ambient" in filename.lower():
            data["transcript"] = ""
            data["language"] = language if language != "auto" else "en"
            return data

        if language and language != "auto":
            data["language"] = language

        return data
