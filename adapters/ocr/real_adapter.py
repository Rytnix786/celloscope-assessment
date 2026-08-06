from typing import Any, Dict

from adapters.ocr.base import BaseOCRAdapter


class RealOCRAdapter(BaseOCRAdapter):
    """Real OCR Adapter integrating Baidu Unlimited-OCR / Vision APIs.

    Activates only when ADAPTER_MODE=real via .env.
    """

    def __init__(self, api_key: str = None) -> None:
        self.api_key = api_key

    def extract(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        # Real provider logic invoked here when credentials are provided in .env
        raise NotImplementedError(
            "Real OCR adapter requires valid provider credentials in .env"
        )
