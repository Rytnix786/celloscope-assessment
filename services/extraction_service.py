from typing import Any, Dict, List

from adapters.ocr.base import BaseOCRAdapter
from services.classifier import LabReportClassifier
from services.normalizers import DateNormalizer, UnitNormalizer, ValueNormalizer


class DocumentExtractionService:
    """Orchestrates lab report classification, OCR extraction, and canonical normalization.

    Strictly zero FastAPI or web framework imports.
    """

    def __init__(self, ocr_adapter: BaseOCRAdapter) -> None:
        self.ocr_adapter = ocr_adapter

    def extract_document(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        ocr_data = self.ocr_adapter.extract(file_bytes, filename)
        full_text = ocr_data.get("full_text", "")

        # 1. Pre-check classification
        is_lab_report, confidence = LabReportClassifier.classify(full_text)
        if not is_lab_report:
            return {
                "is_lab_report": False,
                "confidence": confidence,
                "error": "NOT_A_LAB_REPORT",
                "message": "Uploaded document does not appear to be a medical lab report.",
            }

        # 2. Extract and normalize metadata
        raw_meta = ocr_data.get("meta", {})
        meta = {
            "patient_name": raw_meta.get("patient_name"),
            "age": raw_meta.get("age"),
            "sex": raw_meta.get("sex"),
            "report_date": DateNormalizer.normalize(raw_meta.get("report_date")),
            "lab_name": raw_meta.get("lab_name"),
            "reference_no": raw_meta.get("reference_no"),
        }

        # 3. Extract and normalize results with verbatim raw_line preservation
        raw_lines: List[Dict[str, Any]] = ocr_data.get("raw_lines", [])
        results = []

        for line in raw_lines:
            test_name = line.get("test_name", "Unknown Test")
            raw_value = line.get("raw_value", "")
            raw_unit = line.get("raw_unit")
            raw_ref_range = line.get("raw_reference_range")
            flag = line.get("flag")
            raw_line = line.get("raw_line", "")

            # Run normalizers
            val, qual, vtype = ValueNormalizer.normalize(str(raw_value) if raw_value else "")
            unit = UnitNormalizer.normalize(raw_unit)

            results.append(
                {
                    "test_name": test_name,
                    "value": val,
                    "value_type": vtype,
                    "qualitative_value": qual,
                    "unit": unit,
                    "reference_range": raw_ref_range,
                    "flag": flag,
                    "raw_line": raw_line,  # Preserved verbatim
                }
            )

        return {
            "is_lab_report": True,
            "confidence": confidence,
            "meta": meta,
            "results": results,
        }
