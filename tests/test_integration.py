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


def test_transcribe_endpoint_user_real_voice():
    audio_path = testdata_dir / "audio" / "my-real-voice1.mp3"
    with open(audio_path, "rb") as f:
        response = client.post(
            "/api/v1/transcribe",
            files={"file": ("my-real-voice1.mp3", f, "audio/mp3")},
            data={"language": "en"},
        )
    assert response.status_code == 200
    data = response.json()
    assert "hey so can you hear me" in data["transcript"]
    assert data["audio_duration_seconds"] == 9.38


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


def test_documents_extract_positive_gnuhealth_report():
    report_path = testdata_dir / "documents" / "positive" / "clean_cbc_report.png"
    with open(report_path, "rb") as f:
        response = client.post(
            "/api/v1/documents/extract",
            files={"file": ("clean_cbc_report.png", f, "image/png")},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["is_lab_report"] is True
    assert data["confidence"] == 0.95
    assert data["meta"]["patient_name"] == "Ana Betz"
    assert data["meta"]["report_date"] == "2011-08-25"

    hgb = next(r for r in data["results"] if r["test_name"] == "Hemoglobin")
    assert hgb["value"] == 12.0
    assert hgb["unit"] == "g/dL"

    wbc = next(r for r in data["results"] if r["test_name"] == "WBC Count")
    assert wbc["value"] == 6.7


def test_documents_extract_positive_angled_report():
    report_path = testdata_dir / "documents" / "positive" / "angled_cbc_report.jpg"
    with open(report_path, "rb") as f:
        response = client.post(
            "/api/v1/documents/extract",
            files={"file": ("angled_cbc_report.jpg", f, "image/jpeg")},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["is_lab_report"] is True
    assert data["confidence"] == 0.78
    assert data["meta"]["patient_name"] == "Ana Betz"


def test_documents_extract_positive_dark_report():
    report_path = testdata_dir / "documents" / "positive" / "dark_cbc_report.jpg"
    with open(report_path, "rb") as f:
        response = client.post(
            "/api/v1/documents/extract",
            files={"file": ("dark_cbc_report.jpg", f, "image/jpeg")},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["is_lab_report"] is True
    assert data["confidence"] == 0.70


def test_documents_extract_positive_cropped_report_zero_metadata():
    report_path = testdata_dir / "documents" / "positive" / "cropped_report.jpg"
    with open(report_path, "rb") as f:
        response = client.post(
            "/api/v1/documents/extract",
            files={"file": ("cropped_report.jpg", f, "image/jpeg")},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["is_lab_report"] is True
    assert data["meta"]["patient_name"] is None
    assert data["meta"]["report_date"] is None
    assert data["meta"]["lab_name"] is None


def test_documents_extract_negative_machine_screen_rejection():
    machine_path = testdata_dir / "documents" / "negative" / "cbc_machine_screen.jpg"
    with open(machine_path, "rb") as f:
        response = client.post(
            "/api/v1/documents/extract",
            files={"file": ("cbc_machine_screen.jpg", f, "image/jpeg")},
        )
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["error"] == "NOT_A_LAB_REPORT"
    assert "confidence" in detail


def test_documents_extract_negative_receipt_rejection():
    receipt_path = testdata_dir / "documents" / "negative" / "receipt.jpg"
    with open(receipt_path, "rb") as f:
        response = client.post(
            "/api/v1/documents/extract",
            files={"file": ("receipt.jpg", f, "image/jpeg")},
        )
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["error"] == "NOT_A_LAB_REPORT"
