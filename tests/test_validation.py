from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_transcribe_validation_oversized_file():
    # File larger than 25MB (25 * 1024 * 1024 + 1 bytes)
    big_audio = b"0" * (25 * 1024 * 1024 + 1)
    fake_file = ("huge_audio.wav", big_audio, "audio/wav")
    response = client.post(
        "/api/v1/transcribe",
        files={"file": fake_file},
    )
    assert response.status_code == 413
    detail = response.json()["detail"]
    assert detail["error"] == "FILE_TOO_LARGE"
    assert "25 MB" in detail["message"]


def test_transcribe_validation_unsupported_format():
    fake_file = ("payload.exe", b"executable_binary_content", "application/octet-stream")
    response = client.post(
        "/api/v1/transcribe",
        files={"file": fake_file},
    )
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail["error"] == "UNSUPPORTED_FILE_FORMAT"
    assert "Unsupported audio file format" in detail["message"]


def test_extract_validation_oversized_file():
    big_file = b"0" * (25 * 1024 * 1024 + 1)
    fake_file = ("huge_document.jpg", big_file, "image/jpeg")
    response = client.post(
        "/api/v1/documents/extract",
        files={"file": fake_file},
    )
    assert response.status_code == 413
    detail = response.json()["detail"]
    assert detail["error"] == "FILE_TOO_LARGE"
    assert "25 MB" in detail["message"]


def test_extract_validation_unsupported_format():
    fake_file = ("notes.txt", b"plain text content", "text/plain")
    response = client.post(
        "/api/v1/documents/extract",
        files={"file": fake_file},
    )
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail["error"] == "UNSUPPORTED_FILE_FORMAT"
    assert "Unsupported file extension" in detail["message"]
