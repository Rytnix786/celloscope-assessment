# Architecture Decisions Record (ADR) — Celloscope AI/ML Take-Home

## Decision 1: Canonical Lab Result Schema & Value Discriminator

### Context
Requirement #6 mandates "Every result must include a numeric value", while requirement #7 forbids guessing unparseable values and mandates preserving `raw_line` verbatim. Medical lab reports routinely contain qualitative tests ("Negative", "Reactive") and OCR artifacts that cannot be represented as floating-point numbers without guessing or corrupting domain semantics.

### Decision
We introduced a typed `value_type` discriminator (`numeric`, `qualitative`, `bounded_numeric`, `range`, `unparsed`) alongside a nullable float `value` and string `qualitative_value`.
- For standard numbers (`14.5`, `12,500`, `1.2 x 10^3`), `value` is float (`14.5`, `12500.0`, `1200.0`) and `value_type` is `"numeric"`.
- For qualitative text (`Negative`, `Reactive`), `value` is `null`, `qualitative_value` holds normalized string, and `value_type` is `"qualitative"`.
- For bounded numbers (`<0.5`), `value` holds `0.5`, `qualitative_value` holds `"<0.5"`, and `value_type` is `"bounded_numeric"`.
- For unparseable rows, `value` is `null`, `value_type` is `"unparsed"`, and `raw_line` preserves exact OCR text verbatim.

### Consequences
Resolves the specification contradiction cleanly without data loss, guessing, or API type errors.

---

## Decision 2: OCR Provider Selection & Adapter Isolation

### Context
The lab report extraction endpoint must support both a zero-dependency mock adapter and a high-accuracy real OCR provider.

### Decision
We selected **Baidu Unlimited-OCR / OpenAI Vision** model architectures as our real OCR provider adapter due to superior document structure retention and long-horizon form key-value extraction capabilities. The real provider is strictly isolated inside `adapters/ocr/real_adapter.py` and only instantiated when `ADAPTER_MODE=real` via `.env`.
