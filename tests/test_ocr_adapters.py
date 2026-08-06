from adapters.ocr.factory import get_ocr_adapter
from adapters.ocr.mock_adapter import MockOCRAdapter


def test_mock_ocr_adapter_extraction():
    adapter = MockOCRAdapter()
    data = adapter.extract(b"dummy_bytes", "test.jpg")
    assert "meta" in data
    assert "raw_lines" in data
    assert len(data["raw_lines"]) > 0


def test_ocr_factory_defaults_to_mock():
    adapter = get_ocr_adapter()
    assert isinstance(adapter, MockOCRAdapter)
