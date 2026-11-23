# SpeechBloom AI - Datasets

## Overview

This directory holds speech audio data and annotations used for training and evaluating the SpeechBloom AI pronunciation practice model.

> **⚠️ Important**: Pediatric speech audio is sensitive data. Always collect with appropriate parental consent, store securely, restrict access, and use qualified expert annotation.

## Directory Structure

```
datasets/
├── raw/              # Unprocessed audio recordings
│   ├── hindi/        # Hindi language recordings
│   └── english/      # English language recordings
├── processed/        # Preprocessed audio (normalized, trimmed)
├── annotations/      # CSV annotation files
│   └── speech_labels_template.csv
├── sample/           # Small sample data for testing the pipeline
└── README.md         # This file
```

## Required Dataset Characteristics

For SpeechBloom AI to train an effective pronunciation practice model, datasets should ideally include:

| Feature | Description |
|---------|-------------|
| **Audio recordings** | Children's speech recordings (WAV, 16kHz) |
| **Languages** | Hindi and English |
| **Phoneme labels** | Expert-annotated target and observed phonemes |
| **Speaker metadata** | Pseudonymous speaker ID, age group |
| **Accent/dialect labels** | Regional accent or dialect variation |
| **Error categories** | Substitution, omission, distortion, addition |
| **Recording conditions** | Microphone type, environment noise level |

## Recommended Research Datasets

These publicly available datasets can help build initial audio pipelines:

1. **Speech Accent Archive** — accent variation and pronunciation differences
   - https://accent.gmu.edu/
   - ⚠️ Accent research; not pediatric clinical labels

2. **Mozilla Common Voice** — multilingual speech recognition
   - https://commonvoice.mozilla.org/en/datasets
   - ⚠️ Community-contributed; not pediatric disorder data

3. **Google FLEURS** — multilingual speech experiments
   - https://huggingface.co/datasets/google/fleurs
   - ⚠️ Not a pediatric articulation dataset

4. **AI4Bharat** — Indian language speech research including Hindi
   - https://ai4bharat.iitm.ac.in/
   - ⚠️ Research focus; not clinical pediatric data

> **None of these datasets provide validated pediatric articulation labels.** They are useful for building and testing audio processing pipelines, but a production system requires purpose-collected, ethically approved, expert-annotated data.

## Annotation Format

See `annotations/speech_labels_template.csv` for the expected CSV schema.

## Data Privacy Requirements

- **Parental consent** required before recording any child
- **Pseudonymous IDs** — never store real names with audio
- **Secure storage** — encrypted at rest, access-controlled
- **Right to delete** — parents can request deletion at any time
- **Split by speaker** — train/test splits must separate speakers to prevent data leakage
- **IRB/Ethics approval** — clinical research requires institutional review
