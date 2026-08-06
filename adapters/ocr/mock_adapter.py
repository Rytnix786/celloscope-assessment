import json
from pathlib import Path
from typing import Any, Dict

from adapters.ocr.base import BaseOCRAdapter


class MockOCRAdapter(BaseOCRAdapter):
    """Mock OCR Adapter replaying dedicated, image-accurate fixtures for testdata/documents/ positive and negative sets."""

    def __init__(self, fixtures_dir: Path = None) -> None:
        if fixtures_dir is None:
            self.fixtures_dir = Path(__file__).parent.parent.parent / "testdata" / "fixtures"
        else:
            self.fixtures_dir = fixtures_dir

    def extract(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        fname = filename.lower()

        # 1. Negative / Invalid Document Matchers (Strict Exact Matching)
        if "receipt.jpg" in fname:
            fixture_file = self.fixtures_dir / "neg_receipt_fixture.json"
        elif "invoice.jpg" in fname:
            fixture_file = self.fixtures_dir / "neg_invoice_fixture.json"
        elif "cbc_machine_screen.jpg" in fname or "analyzer_screen.jpg" in fname:
            fixture_file = self.fixtures_dir / "neg_machine_fixture.json"
        elif "blood_typing_card.jpg" in fname or "laboratory_card.jpg" in fname:
            fixture_file = self.fixtures_dir / "neg_card_fixture.json"
        elif "handwritten_note.jpg" in fname or "prescription.jpg" in fname:
            fixture_file = self.fixtures_dir / "neg_handwritten_fixture.json"

        # 2. Positive / Valid Lab Report Matchers (Strict Exact Matching)
        elif "clean_biochemistry_report.png" in fname:
            fixture_file = self.fixtures_dir / "pos_biochem_clean_fixture.json"
        elif "angled_cbc_report.jpg" in fname:
            fixture_file = self.fixtures_dir / "pos_cbc_angled_fixture.json"
        elif "blurred_cbc_report.jpg" in fname:
            fixture_file = self.fixtures_dir / "pos_cbc_blurred_fixture.json"
        elif "dark_cbc_report.jpg" in fname:
            fixture_file = self.fixtures_dir / "pos_cbc_dark_fixture.json"
        elif "cropped_report.jpg" in fname or "cropped_lab_report.jpg" in fname:
            fixture_file = self.fixtures_dir / "pos_cropped_fixture.json"
        elif "clean_cbc_report.png" in fname or "clean_cbc_report.jpg" in fname or "gnuhealth" in fname:
            fixture_file = self.fixtures_dir / "pos_cbc_clean_fixture.json"
        else:
            fixture_file = self.fixtures_dir / "pos_cbc_clean_fixture.json"

        if not fixture_file.exists():
            fixture_file = self.fixtures_dir / "pos_cbc_clean_fixture.json"

        data = json.loads(fixture_file.read_text(encoding="utf-8"))
        return data
