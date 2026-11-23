# Sample Data

This folder is for small sample audio files used to **test the processing pipeline**.

## Important

- Sample files here are **for development and testing only**
- They are **not** validated clinical recordings
- Never present sample/synthetic data as real pediatric speech data
- For actual model training, use ethically collected, expert-annotated datasets

## Usage

Place a few short `.wav` files here (16kHz, mono) to verify that:
1. Audio loading works (`ml/preprocessing.py`)
2. Feature extraction runs (`ml/feature_extraction.py`)
3. The API accepts and processes uploads (`/api/recording`)

## Generating Test Audio

You can generate a simple test tone with Python:

```python
import numpy as np
import soundfile as sf

# Generate a 1-second test tone at 440Hz
sr = 16000
t = np.linspace(0, 1, sr)
audio = 0.5 * np.sin(2 * np.pi * 440 * t)
sf.write('datasets/sample/test_tone.wav', audio, sr)
```
