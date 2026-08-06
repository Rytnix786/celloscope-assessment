from services.classifier import LabReportClassifier


def test_classifier_valid_lab_report():
    sample_text = """
    CENTRAL DIAGNOSTIC LABORATORY
    Patient: John Doe   Age: 45   Sex: M
    Report Date: 2026-08-01   Reference No: REF-9923
    TEST NAME        RESULT     UNIT     REFERENCE RANGE
    Hemoglobin       14.5       g/dL     13.5 - 17.5
    WBC Count        6.5        10^3/µL  4.5 - 11.0
    """
    is_lab, confidence = LabReportClassifier.classify(sample_text)
    assert is_lab is True
    assert confidence > 0.5


def test_classifier_non_lab_report():
    sample_text = "This is a random receipt for coffee and muffins from Star Cafe."
    is_lab, confidence = LabReportClassifier.classify(sample_text)
    assert is_lab is False
    assert confidence < 0.3
