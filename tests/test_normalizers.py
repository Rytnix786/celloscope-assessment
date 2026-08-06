from services.normalizers import DateNormalizer, UnitNormalizer, ValueNormalizer


def test_value_normalizer_numeric():
    val, qual, vtype = ValueNormalizer.normalize("12.5")
    assert val == 12.5
    assert qual is None
    assert vtype == "numeric"


def test_value_normalizer_comma_thousands():
    val, qual, vtype = ValueNormalizer.normalize("12,500")
    assert val == 12500.0
    assert qual is None
    assert vtype == "numeric"


def test_value_normalizer_scientific():
    val, qual, vtype = ValueNormalizer.normalize("1.2 x 10^3")
    assert val == 1200.0
    assert qual is None
    assert vtype == "numeric"


def test_value_normalizer_bounded():
    val, qual, vtype = ValueNormalizer.normalize("<0.5")
    assert val == 0.5
    assert qual == "<0.5"
    assert vtype == "bounded_numeric"


def test_value_normalizer_qualitative():
    val, qual, vtype = ValueNormalizer.normalize("Negative")
    assert val is None
    assert qual == "Negative"
    assert vtype == "qualitative"


def test_value_normalizer_unparsed():
    val, qual, vtype = ValueNormalizer.normalize("Invalid@#$123Text")
    assert val is None
    assert qual is None
    assert vtype == "unparsed"


def test_unit_normalizer():
    assert UnitNormalizer.normalize("gm/dl") == "g/dL"
    assert UnitNormalizer.normalize("g/dL") == "g/dL"
    assert UnitNormalizer.normalize("mg/dl") == "mg/dL"
    assert UnitNormalizer.normalize("mmol/l") == "mmol/L"
    assert UnitNormalizer.normalize("10^3/ul") == "10^3/µL"
    assert UnitNormalizer.normalize("10^3/µL") == "10^3/µL"


def test_date_normalizer():
    assert DateNormalizer.normalize("01/08/2026") == "2026-08-01"
    assert DateNormalizer.normalize("2026-08-01") == "2026-08-01"
    assert DateNormalizer.normalize("01-Aug-2026") == "2026-08-01"
