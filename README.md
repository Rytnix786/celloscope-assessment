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

### Adapter Pattern & Configuration
- **Mock Adapters** (`ADAPTER_MODE=mock`): Replays static disk fixtures with zero network overhead, credentials, or model downloads.
- **Real Adapters** (`ADAPTER_MODE=real`): Activates real STT (Whisper) and OCR (Baidu Unlimited-OCR / Vision) models via environment variables in `.env`.

---

## Document Extraction API (`POST /api/v1/documents/extract`)

### Canonical Schema & Normalization
Medical lab report extraction normalizes values, units, and dates into a canonical representation while preserving `raw_line` verbatim:

- **Value Discriminator (`value_type`)**:
  - `numeric`: Standard numeric values (`14.5`, `12,500` -> `12500.0`, `1.2 x 10^3` -> `1200.0`).
  - `qualitative`: Text-based findings (`Negative`, `Reactive`, `Normal`) stored in `qualitative_value`.
  - `bounded_numeric`: Inequality bounds (`<0.5`) stored with scalar float `0.5` and `qualitative_value="<0.5"`.
  - `unparsed`: Corrupted OCR rows preserved with `raw_line` verbatim without guessing.
- **Units**: Normalized to standard SI/medical representations (`gm/dl` -> `g/dL`, `10^3/ul` -> `10^3/µL`, `mmol/l` -> `mmol/L`).
- **Dates**: Canonical ISO format `YYYY-MM-DD`.

### Non-Lab Report Classifier Pre-Check
Uploads are evaluated before structured extraction. Non-lab report documents (e.g. receipts, random images) are rejected with a structured HTTP 422 `NOT_A_LAB_REPORT` response.

---

## Architectural Decisions
See [DECISIONS.md](DECISIONS.md) for full context on schema trade-offs and adapter design choices.
