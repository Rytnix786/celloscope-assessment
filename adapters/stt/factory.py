from adapters.stt.base import BaseSTTAdapter
from adapters.stt.mock_adapter import MockSTTAdapter
from adapters.stt.real_adapter import RealSTTAdapter
from config import settings


def get_stt_adapter() -> BaseSTTAdapter:
    """Factory creating STT adapter based on configured ADAPTER_MODE."""
    mode = settings.ADAPTER_MODE.lower()
    if mode == "real":
        return RealSTTAdapter()
    return MockSTTAdapter()
