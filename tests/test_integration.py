from pathlib import Path
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
testdata_dir = Path(__file__).parent.parent / "testdata"


def test_transcribe_endpoint_english_speech():
    audio_path = testdata_dir / "audio" / "en_speech_sample1.wav"
    with open(audio_path, "rb") as f:
        response = client.post(
            "/api/v1/transcribe",
            files={"file": ("en_speech_sample1.wav", f, "audio/wav")},
            data={"language": "en"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["transcript"] == "doctor"
    assert data["language"] == "en"
    assert data["audio_duration_seconds"] > 0
    assert "provider" in data


def test_transcribe_endpoint_bengali_speech():
    audio_path = testdata_dir / "audio" / "bn_speech_sample1.wav"
    with open(audio_path, "rb") as f:
        response = client.post(
            "/api/v1/transcribe",
            files={"file": ("bn_speech_sample1.wav", f, "audio/wav")},
            data={"language": "bn"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["transcript"] == "গোলাপ"
    assert data["language"] == "bn"


def test_transcribe_non_speech_silence():
    silence_path = testdata_dir / "audio" / "silence.wav"
    with open(silence_path, "rb") as f:
        response = client.post(
            "/api/v1/transcribe",
            files={"file": ("silence.wav", f, "audio/wav")},
            data={"language": "auto"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["transcript"] == ""
    assert "language" in data


def test_documents_extract_cbc_analyzer_screen_no_hallucination():
    report_path = testdata_dir / "documents" / "clean_lab_report.jpg"
    with open(report_path, "rb") as f:
        response = client.post(
            "/api/v1/documents/extract",
            files={"file": ("clean_lab_report.jpg", f, "image/jpeg")},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["is_lab_report"] is True
    assert data["confidence"] == 0.75

    # Zero metadata hallucination for analyzer screens
    assert data["meta"]["patient_name"] is None
    assert data["meta"]["age"] is None
    assert data["meta"]["report_date"] is None
    assert data["meta"]["lab_name"] is None

    # Exact parameters present on screen
    wbc = next(r for r in data["results"] if r["test_name"] == "WBC")
    assert wbc["value"] == 12.1

    hgb = next(r for r in data["results"] if r["test_name"] == "HGB")
    assert hgb["value"] == 20.4
    assert hgb["unit"] == "g/dL"

    rbc = next(r for r in data["results"] if r["test_name"] == "RBC")
    assert rbc["value"] == 5.53


def test_documents_extract_non_lab_report_rejection():
    receipt_path = testdata_dir / "documents" / "non_lab_receipt.jpg"
    with open(receipt_path, "rb") as f:
        response = client.post(
            "/api/v1/documents/extract",
            files={"file": ("non_lab_receipt.jpg", f, "image/jpeg")},
        )
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["error"] == "NOT_A_LAB_REPORT"
    assert "confidence" in detail
