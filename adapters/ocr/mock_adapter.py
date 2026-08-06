import json
from pathlib import Path
from typing import Any, Dict

from adapters.ocr.base import BaseOCRAdapter


class MockOCRAdapter(BaseOCRAdapter):
    """Mock OCR Adapter replaying dedicated, non-hallucinated fixtures for testdata/documents/ positive and negative sets."""

    def __init__(self, fixtures_dir: Path = None) -> None:
        if fixtures_dir is None:
            self.fixtures_dir = Path(__file__).parent.parent.parent / "testdata" / "fixtures"
        else:
            self.fixtures_dir = fixtures_dir

    def extract(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        fname = filename.lower()

        # Negative / Invalid document matching
        if "receipt" in fname:
            fixture_file = self.fixtures_dir / "neg_receipt_fixture.json"
        elif "invoice" in fname:
            fixture_file = self.fixtures_dir / "neg_invoice_fixture.json"
        elif "machine" in fname or "screen" in fname or "cbc_report.jpg" in fname:
            fixture_file = self.fixtures_dir / "neg_machine_fixture.json"
        elif "card" in fname or "typing" in fname or "crp_test" in fname:
            fixture_file = self.fixtures_dir / "neg_card_fixture.json"
        elif "handwritten" in fname or "prescription" in fname:
            fixture_file = self.fixtures_dir / "neg_handwritten_fixture.json"

        # Positive / Valid report matching
        elif "biochemistry" in fname or "biochem" in fname:
            fixture_file = self.fixtures_dir / "pos_biochem_clean_fixture.json"
        elif "angled" in fname:
            fixture_file = self.fixtures_dir / "pos_cbc_angled_fixture.json"
        elif "blurred" in fname:
            fixture_file = self.fixtures_dir / "pos_cbc_blurred_fixture.json"
        elif "dark" in fname:
            fixture_file = self.fixtures_dir / "pos_cbc_dark_fixture.json"
        elif "cropped" in fname:
            fixture_file = self.fixtures_dir / "pos_cropped_fixture.json"
        elif "clean" in fname or "gnu" in fname or "cbc" in fname:
            fixture_file = self.fixtures_dir / "pos_cbc_clean_fixture.json"
        else:
            fixture_file = self.fixtures_dir / "pos_cbc_clean_fixture.json"

        if not fixture_file.exists():
            fixture_file = self.fixtures_dir / "pos_cbc_clean_fixture.json"

        data = json.loads(fixture_file.read_text(encoding="utf-8"))
        return data
