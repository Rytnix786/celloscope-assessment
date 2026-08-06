import re
from datetime import datetime
from typing import Optional, Tuple


class ValueNormalizer:
    """Normalizes lab result values into a canonical float value, qualitative string, and discriminator type."""

    QUALITATIVE_TERMS = {
        "POSITIVE",
        "NEGATIVE",
        "REACTIVE",
        "NON-REACTIVE",
        "NON REACTIVE",
        "TRACE",
        "PRESENT",
        "ABSENT",
        "NORMAL",
        "HIGH",
        "LOW",
    }

    @classmethod
    def normalize(cls, raw_val: str) -> Tuple[Optional[float], Optional[str], str]:
        if not raw_val or not raw_val.strip():
            return None, None, "unparsed"

        cleaned = raw_val.strip()

        # Qualitative term match
        if cleaned.upper() in cls.QUALITATIVE_TERMS:
            return None, cleaned, "qualitative"

        # Range value match (e.g. 0.8 - 1.2 or 0.8-1.2)
        range_match = re.match(r"^([0-9.]+)\s*-\s*([0-9.]+)$", cleaned)
        if range_match:
            return None, cleaned, "range"

        # Bounded numeric (<0.5, >100, <=10)
        bounded_match = re.match(r"^([<>]=?)\s*([0-9.,]+)$", cleaned)
        if bounded_match:
            try:
                num_str = bounded_match.group(2).replace(",", "")
                scalar = float(num_str)
                return scalar, cleaned, "bounded_numeric"
            except ValueError:
                pass

        # Scientific notation: 1.2 x 10^3 or 1.2 * 10^3 or 1.2e3
        sci_match = re.match(r"^([0-9.]+)\s*(?:x|\*)\s*10\^([0-9]+)$", cleaned, re.IGNORECASE)
        if sci_match:
            try:
                base = float(sci_match.group(1))
                exp = int(sci_match.group(2))
                return base * (10 ** exp), None, "numeric"
            except ValueError:
                pass

        # Standard numeric with comma or dot (e.g. 12,500 or 12.5)
        num_clean = cleaned.replace(",", "")
        try:
            val = float(num_clean)
            return val, None, "numeric"
        except ValueError:
            pass

        # Fallback if no numeric/qualitative format matched
        return None, None, "unparsed"


class UnitNormalizer:
    """Normalizes measurement unit variants into standard canonical representations."""

    MAPPINGS = {
        r"^g[m]?/d[l]?$": "g/dL",
        r"^mg/d[l]?$": "mg/dL",
        r"^mmol/l$": "mmol/L",
        r"^10\^?3/[uµ]l$": "10^3/µL",
        r"^10\^?6/[uµ]l$": "10^6/µL",
        r"^iu/l$": "IU/L",
        r"^%$": "%",
    }

    @classmethod
    def normalize(cls, raw_unit: Optional[str]) -> Optional[str]:
        if not raw_unit or not raw_unit.strip():
            return None

        cleaned = raw_unit.strip()
        for pattern, canonical in cls.MAPPINGS.items():
            if re.match(pattern, cleaned, re.IGNORECASE):
                return canonical

        return cleaned


class DateNormalizer:
    """Normalizes diverse date formats into canonical ISO YYYY-MM-DD format."""

    FORMATS = [
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%d-%b-%Y",
        "%d-%B-%Y",
        "%m/%d/%Y",
        "%d.%m.%Y",
    ]

    @classmethod
    def normalize(cls, raw_date: Optional[str]) -> Optional[str]:
        if not raw_date or not raw_date.strip():
            return None

        cleaned = raw_date.strip()
        for fmt in cls.FORMATS:
            try:
                dt = datetime.strptime(cleaned, fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue

        return cleaned
