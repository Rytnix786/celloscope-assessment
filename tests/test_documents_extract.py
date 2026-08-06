import io
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_extract_lab_report_success():
    fake_file = ("report.jpg", b"fake_lab_report_image_content", "image/jpeg")
    response = client.post(
        "/api/v1/documents/extract",
        files={"file": fake_file},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_lab_report"] is True
    assert "meta" in data
    assert "results" in data
    assert len(data["results"]) > 0

    # Check normalized value and verbatim raw_line preservation
    hgb = next(r for r in data["results"] if r["test_name"] == "Hemoglobin")
    assert hgb["value"] == 14.2
    assert hgb["unit"] == "g/dL"
    assert hgb["value_type"] == "numeric"
    assert "raw_line" in hgb
    assert hgb["raw_line"] != ""


def test_extract_unsupported_format():
    fake_file = ("script.exe", b"binary_content", "application/octet-stream")
    response = client.post(
        "/api/v1/documents/extract",
        files={"file": fake_file},
    )
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail["error"] == "UNSUPPORTED_FILE_FORMAT"


def test_extract_oversized_file():
    # File larger than 25MB (25 * 1024 * 1024 + 1 bytes)
    big_content = b"0" * (25 * 1024 * 1024 + 1)
    fake_file = ("huge_report.jpg", big_content, "image/jpeg")
    response = client.post(
        "/api/v1/documents/extract",
        files={"file": fake_file},
    )
    assert response.status_code == 413
    detail = response.json()["detail"]
    assert detail["error"] == "FILE_TOO_LARGE"
