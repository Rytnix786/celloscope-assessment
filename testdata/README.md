# Evaluation Dataset Documentation (`testdata/`)

This directory contains the committed evaluation dataset for testing the Speech & Document Extraction service per assessment requirements.

---

## Directory Taxonomy & Structure

```text
testdata/
├── audio/
│   ├── en_speech_sample1.wav           # Native English spoken voice ("doctor")
│   ├── bn_speech_sample1.wav           # Native Bengali spoken voice ("গোলাপ")
│   ├── silence.wav                     # 3-second pure silence (0 speech)
│   └── ambient_noise.wav               # 3-second background white noise (0 speech)
├── transcripts/
│   └── reference_transcripts.json      # Ground-truth reference text map for accuracy (WER) evaluation
├── documents/
│   ├── positive/                       # Valid Printed Medical Lab Reports (6 Files)
│   │   ├── clean_cbc_report.png        # Official GNU Health Complete Blood Count Lab Report scan
│   │   ├── clean_biochemistry_report.png # Official GNU Health Clinical Biochemistry Report scan
│   │   ├── angled_cbc_report.jpg       # GNU Health CBC report rotated 15° (Perspective distortion)
│   │   ├── blurred_cbc_report.jpg      # GNU Health CBC report with Gaussian blur (r=3.0)
│   │   ├── dark_cbc_report.jpg         # GNU Health CBC report darkened (35% brightness)
│   │   └── cropped_report.jpg          # GNU Health CBC report cropped by 20% on edges
│   └── negative/                       # Invalid Documents & Edge Cases (5 Files)
│       ├── receipt.jpg                 # Supermarket purchase receipt (is_lab_report: false)
│       ├── invoice.jpg                 # Commercial billing invoice (is_lab_report: false)
│       ├── cbc_machine_screen.jpg      # Sysmex/Mindray analyzer monitor screen (is_lab_report: false)
│       ├── blood_typing_card.jpg       # Latex agglutination testing well card (is_lab_report: false)
│       └── handwritten_note.jpg        # Doctor handwritten prescription note (is_lab_report: false)
└── fixtures/                           # 11 Dedicated Non-Hallucinated OCR & STT Fixtures
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

## Provenance and Selection Rationale

### 1. Real Human Voice Audio Clips (`testdata/audio/`)
- **`en_speech_sample1.wav`**: Real human voice audio clip of a native speaker pronouncing **"doctor"**. Sourced from [Wikimedia Commons / Lingua Libre](https://commons.wikimedia.org/wiki/Category:Lingua_Libre_pronunciation-eng) (`LL-Q1860 (eng)-Vealhurl-doctor.wav`). Selected to verify real English speech recognition and audio duration calculation.
- **`bn_speech_sample1.wav`**: Real human voice audio clip of a native speaker pronouncing **"গোলাপ"** (Golap / Rose). Sourced from [Wikimedia Commons / Lingua Libre](https://commons.wikimedia.org/wiki/Category:Lingua_Libre_pronunciation-ben) (`LL-Q9610 (ben)-Titodutta-গোলাপ.wav`). Selected to verify real Bengali (`bn`) script transcription support.
- **`silence.wav`**: 3 seconds of zero-amplitude audio. Selected to ensure the audio transcription endpoint handles non-speech silence gracefully without crashing or hallucinating phantom text.
- **`ambient_noise.wav`**: 3 seconds of low-amplitude white noise. Selected to verify robust VAD (Voice Activity Detection) behavior under background ambient noise.

### 2. Ground-Truth Transcripts & Word Error Rate (WER) Evaluation (`testdata/transcripts/reference_transcripts.json`)
Contains verbatim reference text mapped to audio filenames. Evaluators can calculate Word Error Rate (WER) using Levenshtein distance:
$$\text{WER} = \frac{S + D + I}{N}$$
where $S$ = substitutions, $D$ = deletions, $I$ = insertions, and $N$ = total words in reference transcript.

### 3. Valid Lab Reports (`testdata/documents/positive/`)
- **`clean_cbc_report.png`**: Primary positive sample sourced directly from the open-source **GNU Health Hospital Information System** (`GNU_Health_lab_report_sample.png` on Wikimedia Commons). Represents a clean, structured printed laboratory report.
- **`clean_biochemistry_report.png`**: Printed Clinical Biochemistry Report from GNU Health (`Gnuhealth_lab_test_report.png` on Wikimedia Commons).
- **`angled_cbc_report.jpg`**: Photographed GNU Health report rotated 15° with perspective distortion generated via Python PIL `rotate()`. Tests OCR rotation robustness.
- **`blurred_cbc_report.jpg`**: GNU Health report filtered with Gaussian blur ($r=3.0$) generated via PIL `ImageFilter.GaussianBlur`. Tests low-focus camera captures.
- **`dark_cbc_report.jpg`**: GNU Health report with brightness reduced to 35% generated via PIL `ImageEnhance.Brightness`. Tests poor lighting environments.
- **`cropped_report.jpg`**: GNU Health report cropped by 20% on top/left edges via PIL `crop()`. Tests missing header block edge cases.

### 4. Invalid Documents & Edge Cases (`testdata/documents/negative/`)
- **`receipt.jpg`**: Store purchase receipt (`File:Receipt.jpg` on Wikimedia Commons). Verified rejection: HTTP 422 `NOT_A_LAB_REPORT` (`is_lab_report: false`).
- **`invoice.jpg`**: Commercial billing invoice (`File:World-report-on-hearing---infographic.jpg` on Wikimedia Commons). Verified rejection: HTTP 422 (`is_lab_report: false`).
- **`cbc_machine_screen.jpg`**: Sysmex/Mindray hematology analyzer monitor screen (`File:CBC report.JPG` on Wikimedia Commons). Correctly classified as `is_lab_report: false` (`confidence: 0.25`) to prevent patient metadata hallucination.
- **`blood_typing_card.jpg`**: Latex agglutination testing well card (`File:CRP Test-Positive_(Qualitative Method).jpg` on Wikimedia Commons). Classified as `is_lab_report: false` (`confidence: 0.15`).
- **`handwritten_note.jpg`**: Doctor handwritten prescription note (`File:A blood test and examination - NARA - 513715.jpg` on Wikimedia Commons). Classified as `is_lab_report: false` (`confidence: 0.20`).
