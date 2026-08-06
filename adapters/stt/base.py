from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseSTTAdapter(ABC):
    """Abstract interface for STT audio transcription adapters."""

    @abstractmethod
    def transcribe(
        self, audio_bytes: bytes, filename: str, language: str
    ) -> Dict[str, Any]:
        """Transcribe audio bytes into transcript text and metadata."""
        pass
