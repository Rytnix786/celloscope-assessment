from typing import Any, Dict

from adapters.stt.base import BaseSTTAdapter


class TranscriptionService:
    """Service orchestrating audio transcription, language selection, and non-speech handling.

    Strictly zero FastAPI or web framework imports.
    """

    def __init__(self, stt_adapter: BaseSTTAdapter) -> None:
        self.stt_adapter = stt_adapter

    def transcribe_audio(
        self, audio_bytes: bytes, filename: str, language: str = "auto"
    ) -> Dict[str, Any]:
        valid_languages = {"bn", "en", "auto"}
        lang = language.lower() if language else "auto"
        if lang not in valid_languages:
            lang = "auto"

        # Delegate to STT adapter
        result = self.stt_adapter.transcribe(
            audio_bytes=audio_bytes, filename=filename, language=lang
        )

        return {
            "transcript": result.get("transcript", ""),
            "language": result.get("language", lang if lang != "auto" else "en"),
            "audio_duration_seconds": result.get("duration_seconds", 0.0),
            "provider": result.get("provider", "mock-stt"),
        }
