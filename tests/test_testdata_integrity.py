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
        "audio/my-real-voice1.mp3",
        "transcripts/reference_transcripts.json",
        "documents/positive/clean_cbc_report.png",
        "documents/positive/clean_biochemistry_report.png",
        "documents/positive/angled_cbc_report.jpg",
        "documents/positive/blurred_cbc_report.jpg",
        "documents/positive/dark_cbc_report.jpg",
        "documents/positive/cropped_report.jpg",
        "documents/negative/receipt.jpg",
        "documents/negative/invoice.jpg",
        "documents/negative/cbc_machine_screen.jpg",
        "documents/negative/blood_typing_card.jpg",
        "documents/negative/handwritten_note.jpg",
        "fixtures/pos_cbc_clean_fixture.json",
        "fixtures/pos_biochem_clean_fixture.json",
        "fixtures/pos_cbc_angled_fixture.json",
        "fixtures/pos_cbc_blurred_fixture.json",
        "fixtures/pos_cbc_dark_fixture.json",
        "fixtures/pos_cropped_fixture.json",
        "fixtures/neg_receipt_fixture.json",
        "fixtures/neg_invoice_fixture.json",
        "fixtures/neg_machine_fixture.json",
        "fixtures/neg_card_fixture.json",
        "fixtures/neg_handwritten_fixture.json",
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
    assert "my-real-voice1.mp3" in data

    assert data["en_speech_sample1.wav"]["language"] == "en"
    assert data["bn_speech_sample1.wav"]["language"] == "bn"
    assert data["my-real-voice1.mp3"]["language"] == "en"
