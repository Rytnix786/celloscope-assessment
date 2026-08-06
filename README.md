# Celloscope AI/ML Take-Home — Speech & Document Extraction

FastAPI microservice providing audio transcription (Bengali & English) and medical lab report extraction capabilities with strict 3-layer architecture (`api/`, `services/`, `adapters/`), typed settings, and zero-dependency mock adapters.

---

## Quick Start

### Running with Docker (Mock Adapters — Zero Credentials / Downloads)
```bash
docker compose up --build
```
Access the service at `http://localhost:8000`.

### Running Locally
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Running Tests
```bash
python -m pytest tests/ -v
```

---

## Architecture & Layer Separation

The application strictly enforces an inward-pointing 3-layer architecture (mechanically verified via AST unit tests):

```text
api/          -> HTTP routing, Pydantic schemas, multipart validation.
services/     -> Business logic & orchestration (strictly ZERO web framework imports).
adapters/     -> Provider & model integrations (the ONLY layer allowed to import provider SDKs).
```

### Adapter Pattern & Deterministic Mock Mode
- **Mock Adapters** (`ADAPTER_MODE=mock`): Per assessment requirements, mock mode replays deterministic, image-accurate OCR responses matching each exact sample document fixture under `testdata/documents/` with zero network overhead, credentials, or model downloads.
- **Real Adapters** (`ADAPTER_MODE=real`): Activates real STT (Whisper) and OCR (Baidu Unlimited-OCR / Vision) models via environment variables in `.env`.

---

## API Endpoints

### 1. Audio Transcription (`POST /api/v1/transcribe`)
- **Multipart Upload**: Audio file (`.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`) + `language` field (`bn`, `en`, or `auto`).
- **Validation**: Rejects files > 25MB and unsupported formats with structured HTTP 413 / HTTP 400 JSON errors.
- **Non-speech Audio**: Silent or ambient noise audio returned with `""` transcript reliably.
- **Returns**: `transcript`, detected `language`, `audio_duration_seconds`, and `provider`.

### 2. Document Extraction (`POST /api/v1/documents/extract`)
- **Multipart Upload**: Image/PDF of medical lab report (`.jpg`, `.jpeg`, `.png`, `.webp`, `.pdf`).
- **Canonical Normalization**:
  - `numeric`: Numbers (`12.0`, `12,500` -> `12500.0`, `1.2 x 10^3` -> `1200.0`).
  - `qualitative`: Text-based findings (`Negative`, `Reactive`) in `qualitative_value`.
  - `bounded_numeric`: Inequality bounds (`<0.5`).
  - `range`: Range values (`0.8 - 1.2`).
  - `unparsed`: Corrupted OCR rows preserved with `raw_line` verbatim without guessing.
- **Units & Dates**: Standard SI units (`gm/dl` -> `g/dL`, `10^3/ul` -> `10^3/µL`) and ISO dates (`YYYY-MM-DD`).
- **Classifier Pre-check**: Rejects non-lab documents (analyzer screens, testing cards, invoices, receipts, prescriptions) with HTTP 422 `NOT_A_LAB_REPORT` response.

---

## Test Data Sourcing (`testdata/`)

Test data is committed under `testdata/` with full provenance documented in [testdata/README.md](testdata/README.md):
- **Audio Clips**: Real native human voice clips for Bengali (`bn_speech_sample1.wav`) and English (`en_speech_sample1.wav`) sourced from Wikimedia Commons Lingua Libre, plus synthetic silence (`silence.wav`) and white noise (`ambient_noise.wav`).
- **Reference Transcripts**: Ground-truth text map in `testdata/transcripts/reference_transcripts.json` for Word Error Rate (WER) accuracy calculation.
- **Document Images**: Sourced from official **GNU Health Hospital Information System** samples (`clean_cbc_report.png`, `clean_biochemistry_report.png`), PIL transformed variants (angles, blur, darkness, cropping), and negative non-reports (`receipt.jpg`, `invoice.jpg`, `cbc_machine_screen.jpg`, `blood_typing_card.jpg`, `handwritten_note.jpg`).

---

## Known Limitations & Disclosed Gaps

Per assessment guidelines, we explicitly disclose the following known edge cases and design boundaries:

1. **Severely Truncated Lab Reports**: If a photographed report has its header block completely cut off (`cropped_report.jpg`), `meta` header fields (`patient_name`, `report_date`, `lab_name`) return `null` rather than guessing or fabricating metadata.
2. **Exotic Medical Units**: Unrecognized or non-standard regional measurement units fall back to being preserved verbatim without forced normalization.
3. **Overlapping Multi-Speaker Speech**: Heavy multi-speaker crosstalk in audio recordings can increase Word Error Rate (WER) compared to single-speaker clinical dictations.
4. **Real Adapter GPU Requirements**: Running real local STT/OCR model adapters (`ADAPTER_MODE=real`) locally requires an NVIDIA GPU with at least 8GB VRAM or cloud API keys configured in `.env`.

---

## Architectural Decisions Record
See [DECISIONS.md](DECISIONS.md) for full context on model selection, schema trade-offs, non-speech VAD strategy, and layer separation enforcement.
