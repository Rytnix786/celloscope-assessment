from typing import Tuple


class LabReportClassifier:
    """Classifies whether a document's extracted text is a valid medical lab report or diagnostic screen."""

    KEYWORD_WEIGHTS = {
        "LABORATORY": 0.25,
        "DIAGNOSTIC": 0.20,
        "PATIENT": 0.20,
        "REFERENCE NO": 0.20,
        "TEST NAME": 0.25,
        "RESULT": 0.20,
        "REFERENCE RANGE": 0.25,
        "UNIT": 0.15,
        "HEMOGLOBIN": 0.20,
        "PATHOLOGY": 0.20,
        "BLOOD": 0.15,
        "WBC": 0.20,
        "RBC": 0.20,
        "HGB": 0.20,
        "HCT": 0.15,
        "PLT": 0.20,
        "CRP": 0.25,
    }

    @classmethod
    def classify(cls, text: str) -> Tuple[bool, float]:
        if not text or not text.strip():
            return False, 0.0

        upper_text = text.upper()
        total_score = 0.0

        for keyword, weight in cls.KEYWORD_WEIGHTS.items():
            if keyword in upper_text:
                total_score += weight

        # Cap confidence at 1.0
        confidence = min(1.0, total_score)
        is_lab_report = confidence >= 0.40

        return is_lab_report, round(confidence, 2)
