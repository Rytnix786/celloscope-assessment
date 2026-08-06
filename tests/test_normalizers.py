from services.normalizers import DateNormalizer, UnitNormalizer, ValueNormalizer


def test_normalize_standard_numeric():
    val, qual, vtype = ValueNormalizer.normalize("12.5")
    assert val == 12.5
    assert qual is None
    assert vtype == "numeric"


def test_normalize_comma_thousands():
    val, qual, vtype = ValueNormalizer.normalize("12,500")
    assert val == 12500.0
    assert qual is None
    assert vtype == "numeric"


def test_normalize_scientific_notation():
    val, qual, vtype = ValueNormalizer.normalize("1.2 x 10^3")
    assert val == 1200.0
    assert qual is None
    assert vtype == "numeric"


def test_normalize_bounded_numeric():
    val, qual, vtype = ValueNormalizer.normalize("<0.5")
    assert val == 0.5
    assert qual == "<0.5"
    assert vtype == "bounded_numeric"


def test_normalize_range_value():
    val, qual, vtype = ValueNormalizer.normalize("0.8 - 1.2")
    assert val is None
    assert qual == "0.8 - 1.2"
    assert vtype == "range"


def test_normalize_unparseable_fallback():
    val, qual, vtype = ValueNormalizer.normalize("Corrupted Text 12#$%")
    assert val is None
    assert qual is None
    assert vtype == "unparsed"


def test_normalize_units_and_dates():
    assert UnitNormalizer.normalize("gm/dl") == "g/dL"
    assert UnitNormalizer.normalize("10^3/ul") == "10^3/µL"
    assert UnitNormalizer.normalize("mmol/l") == "mmol/L"
    assert DateNormalizer.normalize("12/08/2026") == "2026-08-12"
    assert DateNormalizer.normalize("12-Aug-2026") == "2026-08-12"
