import json
from pathlib import Path


def test_testdata_files_exist_and_non_empty():
    testdata_dir = Path(__file__).parent.parent / "testdata"
    assert testdata_dir.exists()

    required_files = [
        "README.md",
        "audio/en_speech_sample1.wav",
        "audio/bn_speech_sample1.wav",
        "audio/silence.wav",
        "audio/ambient_noise.wav",
        "transcripts/reference_transcripts.json",
        "documents/clean_lab_report.jpg",
        "documents/angled_lab_report.jpg",
        "documents/gnuhealth_lab_report.png",
        "documents/non_lab_receipt.jpg",
        "fixtures/sample_lab_report.json",
        "fixtures/sample_transcription.json",
    ]

    for rel_path in required_files:
        file_path = testdata_dir / rel_path
        assert file_path.exists(), f"Missing required testdata file: {rel_path}"
        assert file_path.stat().st_size > 0, f"File is empty: {rel_path}"


def test_reference_transcripts_json_schema():
    ref_file = Path(__file__).parent.parent / "testdata" / "transcripts" / "reference_transcripts.json"
    data = json.loads(ref_file.read_text(encoding="utf-8"))
    assert "en_speech_sample1.wav" in data
    assert "bn_speech_sample1.wav" in data
    assert "silence.wav" in data
    assert "ambient_noise.wav" in data

    assert data["en_speech_sample1.wav"]["language"] == "en"
    assert data["bn_speech_sample1.wav"]["language"] == "bn"
