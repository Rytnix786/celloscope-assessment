import json
from pathlib import Path
from typing import Any, Dict

from adapters.ocr.base import BaseOCRAdapter


class MockOCRAdapter(BaseOCRAdapter):
    """Mock OCR Adapter replaying disk fixtures with zero network calls or model downloads."""

    def __init__(self, fixture_path: Path = None) -> None:
        if fixture_path is None:
            self.fixture_path = (
                Path(__file__).parent.parent.parent
                / "testdata"
                / "fixtures"
                / "sample_lab_report.json"
            )
        else:
            self.fixture_path = fixture_path

    def extract(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        fname_lower = filename.lower()
        if "receipt" in fname_lower or "non_lab" in fname_lower:
            return {
                "full_text": "STAR CAFE & BAKERY Receipt #109283 Espresso Coffee $4.50 Chocolate Muffin $7.00 Total Paid $11.50 Thank you for visiting",
                "meta": {},
                "raw_lines": [],
            }

        if not self.fixture_path.exists():
            raise FileNotFoundError(f"Mock OCR fixture not found at {self.fixture_path}")

        data = json.loads(self.fixture_path.read_text(encoding="utf-8"))
        return data
