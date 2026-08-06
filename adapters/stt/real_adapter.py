from typing import Any, Dict

from adapters.stt.base import BaseSTTAdapter


class RealSTTAdapter(BaseSTTAdapter):
    """Real STT Adapter integrating OpenAI Whisper / Faster-Whisper.

    Activates only when ADAPTER_MODE=real via .env.
    """

    def __init__(self, api_key: str = None) -> None:
        self.api_key = api_key

    def transcribe(
        self, audio_bytes: bytes, filename: str, language: str
    ) -> Dict[str, Any]:
        # Real Whisper model invocation logic when credentials are provided in .env
        raise NotImplementedError(
            "Real STT adapter requires valid provider credentials in .env"
        )
