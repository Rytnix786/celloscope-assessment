import json
from pathlib import Path
from typing import Any, Dict

from adapters.ocr.base import BaseOCRAdapter


class MockOCRAdapter(BaseOCRAdapter):
    """Mock OCR Adapter replaying dedicated, non-hallucinated fixtures matching testdata/documents/."""

    def __init__(self, fixtures_dir: Path = None) -> None:
        if fixtures_dir is None:
            self.fixtures_dir = Path(__file__).parent.parent.parent / "testdata" / "fixtures"
        else:
            self.fixtures_dir = fixtures_dir

    def extract(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        fname = filename.lower()

        if "receipt" in fname or "non_lab" in fname:
            fixture_file = self.fixtures_dir / "non_lab_receipt_fixture.json"
        elif "angled" in fname or "crp" in fname:
            fixture_file = self.fixtures_dir / "angled_lab_report_fixture.json"
        elif "gnuhealth" in fname or "gnu" in fname:
            fixture_file = self.fixtures_dir / "gnuhealth_lab_report_fixture.json"
        elif "clean" in fname or "cbc" in fname or "sample_lab_report" in fname:
            fixture_file = self.fixtures_dir / "clean_lab_report_fixture.json"
        else:
            fixture_file = self.fixtures_dir / "clean_lab_report_fixture.json"

        if not fixture_file.exists():
            # Fallback to default fixture if file not found
            fixture_file = self.fixtures_dir / "sample_lab_report.json"

        data = json.loads(fixture_file.read_text(encoding="utf-8"))
        return data
