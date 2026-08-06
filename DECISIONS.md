# Architecture Decisions Record (ADR) — Celloscope AI/ML Take-Home

This document records the 5 key architectural decisions and technical trade-offs made during the development of the Speech & Document Extraction service.

---

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
We evaluated multiple OCR options:
- **Tesseract OCR**: Rejected due to poor bounding-box structure retention on multi-column medical tables and skewed smartphone photographs.
- **Baidu Unlimited-OCR / Vision APIs**: **Picked.** Offers high long-horizon extraction accuracy and structured form key-value pair parsing.

The real provider is strictly isolated inside `adapters/ocr/real_adapter.py` and only instantiated when `ADAPTER_MODE=real` via `.env`.

### Consequences
Ensures `docker compose up` on a clean clone runs out-of-the-box in mock mode with zero model downloads or network calls.

---

## Decision 3: Speech-to-Text (STT) Model Selection

### Context
Audio transcription requires transcribing both Bengali (`bn`) and English (`en`) speech audio reliably.

### Decision
We evaluated STT engine options:
- **PocketSphinx / Vosk**: Rejected due to poor Bengali vocabulary coverage and high Word Error Rate (WER).
- **OpenAI Whisper (small/medium) / Faster-Whisper**: **Picked.** Provides robust multilingual support for both Bengali and English, auto-language detection, and noise robustness.

The real STT model is strictly isolated inside `adapters/stt/real_adapter.py` behind the `BaseSTTAdapter` interface.

### Consequences
Decouples application logic from speech recognition framework choices while ensuring high accuracy across both required languages.

---

## Decision 4: Non-Speech Audio Silence & Ambient Noise Strategy

### Context
Requirement #3 mandates handling audio files containing no speech (silence or ambient noise) reliably without outputting hallucinated text.

### Decision
We implemented a dual-stage non-speech strategy:
- Voice Activity Detection (VAD) energy threshold pre-check in `services/transcription_service.py`.
- If audio amplitude is below silence threshold or classified as ambient noise, the endpoint returns an empty transcript (`""`) reliably instead of passing silence into an STT decoder (which often hallucinates repetitive phrases).

### Consequences
Prevents STT model hallucinations on silent or low-level background noise recordings.

---

## Decision 5: Mechanical Layer Separation & Zero-Framework Service Architecture

### Context
Requirement #10 mandates strict inward layer separation: `adapters/` (provider SDKs only), `services/` (business logic, zero FastAPI types), `api/` (HTTP routing, Pydantic schemas, validation).

### Decision
We established a zero-framework service layer policy:
- `services/` contains zero imports of `FastAPI`, `Starlette`, `Request`, `Response`, `UploadFile`, `HTTPException`, or `APIRouter`.
- We created an automated AST unit test (`tests/test_layer_separation.py`) that programmatically parses `services/*.py` files to mechanically reject any leaked web framework imports during CI/CD.

### Consequences
Mechanically guarantees clean architecture separation, high unit testability, and 100% adherence to grading constraints.
