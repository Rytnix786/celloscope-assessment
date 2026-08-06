from adapters.ocr.base import BaseOCRAdapter
from adapters.ocr.mock_adapter import MockOCRAdapter
from adapters.ocr.real_adapter import RealOCRAdapter
from config import settings


def get_ocr_adapter() -> BaseOCRAdapter:
    """Factory creating OCR adapter based on configured ADAPTER_MODE."""
    mode = settings.ADAPTER_MODE.lower()
    if mode == "real":
        return RealOCRAdapter()
    return MockOCRAdapter()
