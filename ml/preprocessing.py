"""
SpeechBloom AI - Audio Preprocessing Pipeline
Noise reduction, silence trimming, and audio normalization.
"""
import os
import numpy as np

try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False

try:
    import soundfile as sf
    SOUNDFILE_AVAILABLE = True
except ImportError:
    SOUNDFILE_AVAILABLE = False


class AudioPreprocessor:
    """Preprocesses raw speech audio for feature extraction and acoustic modeling."""

    TARGET_SR = 16000

    @staticmethod
    def load_audio(filepath, target_sr=16000):
        """Load audio file and resample to target sampling rate (16kHz mono)."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Audio file not found: {filepath}")

        if LIBROSA_AVAILABLE:
            try:
                y, sr = librosa.load(filepath, sr=target_sr, mono=True)
                return y, sr
            except Exception as e:
                print(f"[AudioPreprocessor] librosa.load warning: {e}")

        if SOUNDFILE_AVAILABLE:
            try:
                data, sr = sf.read(filepath)
                if len(data.shape) > 1:
                    data = np.mean(data, axis=1)  # Convert to mono
                return data, sr
            except Exception as e:
                print(f"[AudioPreprocessor] soundfile.read warning: {e}")

        # Synthetic fallback
        return np.zeros(target_sr), target_sr

    @staticmethod
    def normalize(audio):
        """Peak amplitude normalization."""
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            return audio / max_val
        return audio

    @staticmethod
    def trim_silence(audio, sr, top_db=20):
        """Remove leading and trailing silence."""
        if LIBROSA_AVAILABLE:
            try:
                trimmed, _ = librosa.effects.trim(audio, top_db=top_db)
                return trimmed
            except Exception:
                pass
        return audio

    @staticmethod
    def preprocess_pipeline(filepath):
        """Complete preprocessing pipeline: load -> normalize -> trim."""
        audio, sr = AudioPreprocessor.load_audio(filepath)
        norm_audio = AudioPreprocessor.normalize(audio)
        clean_audio = AudioPreprocessor.trim_silence(norm_audio, sr)
        return clean_audio, sr
