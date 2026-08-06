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
│   ├── clean_lab_report.jpg            # Real Complete Blood Count (CBC) diagnostic lab report scan
│   ├── angled_lab_report.jpg           # Real CRP qualitative blood test result photograph
│   ├── gnuhealth_lab_report.png        # Real GNU Health electronic clinical pathology report
│   └── non_lab_receipt.jpg             # Real store receipt photo for negative classifier testing
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

### 3. Real Document Images (`testdata/documents/`)
- **`clean_lab_report.jpg`**: Real digital photograph scan of an actual Complete Blood Count (CBC) diagnostic clinical pathology lab report. Sourced from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:CBC_report.JPG) (`File:CBC report.JPG`). Selected to verify high-accuracy structured table parsing.
- **`angled_lab_report.jpg`**: Real photograph of a Qualitative CRP Blood Test result strip. Sourced from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:CRP_Test-Positive_(Qualitative_Method).jpg) (`File:CRP Test-Positive (Qualitative Method).jpg`). Selected to test real qualitative findings (`"Positive"`) and photographed test strips.
- **`gnuhealth_lab_report.png`**: Real electronic health record lab report layout from GNU Health open-source clinical pathology system. Sourced from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Gnuhealth_lab_test_report.png) (`File:Gnuhealth lab test report.png`). Selected to test digital EHR report layouts.
- **`non_lab_receipt.jpg`**: Real store purchase receipt photo. Sourced from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Receipt.jpg) (`File:Receipt.jpg`). Selected to verify that the lab report pre-check classifier rejects non-lab document uploads with HTTP 422 `NOT_A_LAB_REPORT` instead of outputting garbage fields.
