from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseOCRAdapter(ABC):
    """Abstract interface for OCR document extraction adapters."""

    @abstractmethod
    def extract(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """Extract raw structured OCR data and lines from document file bytes."""
        pass
