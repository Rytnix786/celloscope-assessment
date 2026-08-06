# Medical Speech Transcription & Lab Report Extraction Service

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green.svg)](https://fastapi.tiangolo.com/)
[![Docker Compose](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)
[![CI/CD Pipeline](https://github.com/Rytnix786/celloscope-assessment/actions/workflows/ci.yml/badge.svg)](https://github.com/Rytnix786/celloscope-assessment/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/Tests-25%20Passed-brightgreen.svg)]()

FastAPI microservice providing multi-lingual audio transcription (Bengali `bn` and English `en`) and medical lab report extraction capabilities. Built with a strict 3-layer architecture (`api/`, `services/`, `adapters/`), typed configuration settings, zero-credential mock mode, and non-hallucinating canonical value normalization.

---

## Executive Summary & Features

1. **Audio Transcription Endpoint (`POST /api/v1/transcribe`)**:
   - Accepts `.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg` audio files up to 25MB.
   - Supports Bengali (`bn`), English (`en`), and automatic language identification (`auto`).
   - Handles silent and background noise audio gracefully returning empty transcript without hallucination.
   - Calculates exact audio duration in seconds.

2. **Document Extraction Endpoint (`POST /api/v1/documents/extract`)**:
   - Accepts `.jpg`, `.jpeg`, `.png`, `.webp`, `.pdf` lab report files up to 10MB.
   - Rejects non-lab documents (analyzer screens, testing cards, invoices, receipts, prescriptions) with HTTP 422 `NOT_A_LAB_REPORT`.
   - Normalizes test values into canonical types (`numeric`, `qualitative`, `bounded_numeric`, `range`, `unparsed`).
   - Normalizes measurement units (`gm/dl` -> `g/dL`, `10^3/ul` -> `10^3/µL`) and dates (`YYYY-MM-DD`).
   - Preserves verbatim unparseable text in `raw_line` without forced guessing.
   - Never fabricates metadata on cropped or missing report headers (`null` preservation).

3. **Production Architecture & CI/CD Pipeline**:
   - **Strict Layer Separation**: Verified mechanically via AST parsing unit tests (`tests/test_layer_separation.py`). `services/` contains zero FastAPI/Starlette imports. `adapters/` is the only layer allowed to import model SDKs.
   - **Multi-Stage CI/CD Pipeline**: Automated GitHub Actions pipeline (`.github/workflows/ci.yml`) enforcing 4 quality gates: Ruff linting & Mypy typing, AST layer separation audit, multi-Python (3.11, 3.12) pytest matrix with coverage, and Docker build validation.
   - **Zero-Credential Docker Boot**: `docker compose up` boots out of the box in `ADAPTER_MODE=mock` with zero network calls, credentials, or model downloads.

---

## Quick Start & Setup Guide

### 1. Running with Docker Compose (Recommended)
```bash
# Clone the repository
git clone https://github.com/Rytnix786/celloscope-assessment.git
cd celloscope-assessment

# Boot container in zero-credential mock mode
docker compose up --build
```
The API interactive documentation will be available at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

### 2. Local Environment Setup & Makefile Commands

```bash
# Create and activate virtual environment
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate

# On Windows PowerShell:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Available Makefile Commands:
make test        # Run unit and integration test suite
make docker-up   # Start service via Docker Compose
make lint        # Run layer separation AST audit test
```

---

### 3. Running the Test Suite
```bash
# Run all 25 automated unit, integration, and layer separation tests
python -m pytest tests/ -v
```

---

## CI/CD Pipeline Architecture (`.github/workflows/ci.yml`)

The repository uses GitHub Actions for continuous integration with 4 sequential quality jobs:

```text
[Git Push / PR] ──► Job 1: Ruff Linting & Mypy Type Checker
                ──► Job 2: Layer Separation AST Audit & Secret Leak Guard
                ──► Job 3: Pytest Matrix (Python 3.11 & 3.12) + Coverage
                └──► Job 4: Docker Compose Build Verification
```

---

## Evaluation Dataset Documentation (`testdata/`)

The repository includes an interview-grade evaluation dataset committed under `testdata/` with full provenance documented in [testdata/README.md](testdata/README.md).

```text
testdata/
├── audio/
│   ├── en_speech_sample1.wav           # Native English spoken voice ("doctor")
│   ├── bn_speech_sample1.wav           # Native Bengali spoken voice ("গোলাপ")
│   ├── silence.wav                     # 3-second zero-amplitude silence
│   ├── ambient_noise.wav               # 3-second background white noise
│   └── my-real-voice1.mp3              # Real user voice recording ("hey so can you hear me...")
├── transcripts/
│   └── reference_transcripts.json      # Ground-truth reference text map for WER accuracy evaluation
├── documents/
│   ├── positive/                       # Valid Printed Medical Lab Reports (6 Files)
│   │   ├── clean_cbc_report.png        # Official GNU Health Complete Blood Count scan (Ana Betz)
│   │   ├── clean_biochemistry_report.png # Official GNU Health Clinical Biochemistry scan
│   │   ├── angled_cbc_report.jpg       # GNU Health CBC report rotated 15° (PIL transformation)
│   │   ├── blurred_cbc_report.jpg      # GNU Health CBC report with Gaussian blur (r=3.0)
│   │   ├── dark_cbc_report.jpg         # GNU Health CBC report darkened (35% brightness)
│   │   └── cropped_report.jpg          # GNU Health CBC report cropped by 20% on edges
│   └── negative/                       # Invalid Documents & Edge Cases (5 Files)
│       ├── receipt.jpg                 # Supermarket purchase receipt (is_lab_report: false)
│       ├── invoice.jpg                 # Commercial billing invoice (is_lab_report: false)
│       ├── cbc_machine_screen.jpg      # Sysmex/Mindray analyzer monitor screen (is_lab_report: false)
│       ├── blood_typing_card.jpg       # Latex agglutination testing well card (is_lab_report: false)
│       └── handwritten_note.jpg        # Authentic 1965 handwritten doctor prescription note (is_lab_report: false)
└── fixtures/                           # Dedicated Non-Hallucinated Mock OCR & STT Fixtures
    ├── pos_cbc_clean_fixture.json
    ├── pos_biochem_clean_fixture.json
    ├── pos_cbc_angled_fixture.json
    ├── pos_cbc_blurred_fixture.json
    ├── pos_cbc_dark_fixture.json
    ├── pos_cropped_fixture.json
    ├── neg_receipt_fixture.json
    ├── neg_invoice_fixture.json
    ├── neg_machine_fixture.json
    ├── neg_card_fixture.json
    ├── neg_handwritten_fixture.json
    └── sample_transcription.json
```

---

## Canonical Normalization Engine Rules

Medical test values are extracted and normalized deterministically according to strict mathematical and linguistic rules:

| Source OCR Line Format | Extracted Value | `value_type` | `qualitative_value` | Standardized Unit | Flag |
|---|---|---|---|---|---|
| `Hemoglobin 12.0 g/dL` | `12.0` | `numeric` | `null` | `g/dL` | `Normal` |
| `Platelet Count 12,500 /uL` | `12500.0` | `numeric` | `null` | `10^3/µL` | `Low` |
| `RBC 1.2 x 10^6 /uL` | `1200000.0` | `numeric` | `null` | `10^6/µL` | `Normal` |
| `HBsAg Negative` | `null` | `qualitative` | `"Negative"` | `null` | `Normal` |
| `hs-CRP <0.5 mg/L` | `0.5` | `bounded_numeric` | `null` | `mg/L` | `Normal` |
| `Serum Sodium 135 - 145` | `135.0` | `range` | `null` | `mmol/L` | `Normal` |
| `Corrupted OCR row ###` | `null` | `unparsed` | `null` | `null` | `null` |

---

## Disclosed Known Limitations & Gaps

Per assessment guidelines, we explicitly disclose the following known edge cases and system boundaries:

1. **Severely Truncated Header Blocks**: When a lab report's header section is completely cropped out (`cropped_report.jpg`), `meta` header fields (`patient_name`, `report_date`, `lab_name`) return `null` rather than guessing or fabricating metadata.
2. **Exotic Regional Units**: Non-standard measurement units fall back to being preserved verbatim without forced normalization.
3. **Overlapping Multi-Speaker Audio**: Heavy multi-speaker crosstalk in audio recordings can increase Word Error Rate (WER) compared to single-speaker clinical dictations.
4. **Real Adapter GPU Requirements**: Running real local STT/OCR model adapters (`ADAPTER_MODE=real`) locally requires an NVIDIA GPU with at least 8GB VRAM or cloud API keys configured in `.env`.

---

## Architectural Decision Records (ADRs)

See [DECISIONS.md](DECISIONS.md) for detailed design trade-offs:
- **ADR-001**: Clean 3-Layer Architecture (`api/`, `services/`, `adapters/`).
- **ADR-002**: Discriminator Pattern for Value Normalization (`value_type`).
- **ADR-003**: Non-Speech Audio Silence Handling in STT Service.
- **ADR-004**: Classifier Pre-Check for Non-Lab Document Rejection.
- **ADR-005**: Mock Adapter Strategy & Environment Configuration.
