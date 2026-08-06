# Test Data Documentation (`testdata/`)

This directory contains the committed evaluation dataset for testing the Speech & Document Extraction service per assessment requirements.

---

## Directory Structure

```text
testdata/
├── README.md                           # Sourcing origins, selection rationale, and WER evaluation
├── audio/
│   ├── en_speech_sample1.wav           # Real human voice English speech audio ("doctor")
│   ├── bn_speech_sample1.wav           # Real human voice Bengali speech audio ("গোলাপ")
│   ├── silence.wav                     # 3-second pure silence (0 speech)
│   └── ambient_noise.wav               # 3-second background white noise (0 speech)
├── transcripts/
│   └── reference_transcripts.json      # Ground-truth reference text map for accuracy (WER) evaluation
├── documents/
│   ├── clean_lab_report.png            # High-resolution medical lab report image
│   ├── angled_lab_report.png           # Rotated/skewed lab report image simulating phone photography
│   └── non_lab_receipt.png             # Non-medical cafe receipt for negative classifier testing
└── fixtures/
    ├── sample_lab_report.json          # Mock OCR fixture data
    └── sample_transcription.json       # Mock STT fixture data
```

---

## Origins and Selection Rationale

### 1. Real Human Voice Audio Clips (`testdata/audio/`)
- **`en_speech_sample1.wav`**: Real human voice audio clip of a native speaker pronouncing **"doctor"**. Sourced from [Wikimedia Commons / Lingua Libre](https://commons.wikimedia.org/wiki/Category:Lingua_Libre_pronunciation-eng) (`LL-Q1860 (eng)-Vealhurl-doctor.wav`). Selected to verify real English speech recognition and audio duration calculation.
- **`bn_speech_sample1.wav`**: Real human voice audio clip of a native speaker pronouncing **"গোলাপ"** (Golap / Rose). Sourced from [Wikimedia Commons / Lingua Libre](https://commons.wikimedia.org/wiki/Category:Lingua_Libre_pronunciation-ben) (`LL-Q9610 (ben)-Titodutta-গোলাপ.wav`). Selected to verify real Bengali (`bn`) script transcription support.
- **`silence.wav`**: 3 seconds of zero-amplitude audio. Selected to ensure the audio transcription endpoint handles non-speech silence gracefully without crashing or hallucinating phantom text.
- **`ambient_noise.wav`**: 3 seconds of low-amplitude white noise. Selected to verify robust VAD (Voice Activity Detection) behavior under background ambient noise.

### 2. Ground-Truth Transcripts (`testdata/transcripts/reference_transcripts.json`)
Contains verbatim reference text mapped to audio filenames. Evaluators can calculate Word Error Rate (WER) using Levenshtein distance:
$$\text{WER} = \frac{S + D + I}{N}$$
where $S$ = substitutions, $D$ = deletions, $I$ = insertions, and $N$ = total words in reference transcript.

### 3. Document Images (`testdata/documents/`)
- **`clean_lab_report.png`**: High-quality digital rendering of a Complete Blood Count (CBC) & metabolic lab report with header block and results table.
- **`angled_lab_report.png`**: Rotated (4° skew) with background noise to simulate smartphone photography taken at an angle in real-world clinic settings.
- **`non_lab_receipt.png`**: Non-medical cafe receipt image. Selected to verify that the lab report pre-check classifier rejects non-lab uploads with HTTP 422 `NOT_A_LAB_REPORT` instead of outputting garbage fields.
