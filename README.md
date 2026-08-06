# Celloscope AI/ML Take-Home — Speech & Document Extraction

FastAPI microservice providing audio transcription and medical lab report extraction capabilities with strict 3-layer architecture (`api/`, `services/`, `adapters/`), typed settings, and zero-dependency mock adapters.

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
  - `numeric`: Numbers (`12.5`, `12,500` -> `12500.0`, `1.2 x 10^3` -> `1200.0`).
  - `qualitative`: Text-based findings (`Negative`, `Reactive`) in `qualitative_value`.
  - `bounded_numeric`: Inequality bounds (`<0.5`).
  - `range`: Range values (`0.8 - 1.2`).
  - `unparsed`: Corrupted OCR rows preserved with `raw_line` verbatim without guessing.
- **Units & Dates**: Standard SI units (`gm/dl` -> `g/dL`, `10^3/ul` -> `10^3/µL`) and ISO dates (`YYYY-MM-DD`).
- **Classifier Pre-check**: Rejects non-lab documents with HTTP 422 `NOT_A_LAB_REPORT` response.

---

## Architectural Decisions Record
See [DECISIONS.md](DECISIONS.md) for full context on schema trade-offs and adapter design choices.
