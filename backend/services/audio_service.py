"""
SpeechBloom AI - Audio Processing Service
Handles audio storage, metadata inspection, format conversion, and acoustic feature extraction.
"""
import os
import tempfile
import numpy as np

# Optional scientific imports with safe fallbacks
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

try:
    import speech_recognition as sr_lib
    SPEECH_REC_AVAILABLE = True
except ImportError:
    SPEECH_REC_AVAILABLE = False


class AudioService:
    """Service for handling audio file operations and feature extraction."""

    @staticmethod
    def save_audio(audio_bytes, filename, upload_folder):
        """Save raw audio bytes to destination folder."""
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        with open(filepath, 'wb') as f:
            f.write(audio_bytes)
        return filepath

    @staticmethod
    def get_audio_info(filepath):
        """Extract basic duration and sampling properties."""
        file_size = os.path.getsize(filepath) if os.path.exists(filepath) else 0

        if SOUNDFILE_AVAILABLE and os.path.exists(filepath):
            try:
                info = sf.info(filepath)
                return {
                    'duration': round(float(info.duration), 2),
                    'sample_rate': int(info.samplerate),
                    'channels': int(info.channels),
                    'file_size': file_size
                }
            except Exception:
                pass

        if LIBROSA_AVAILABLE and os.path.exists(filepath):
            try:
                duration = librosa.get_duration(path=filepath)
                return {
                    'duration': round(float(duration), 2),
                    'sample_rate': 16000,
                    'channels': 1,
                    'file_size': file_size
                }
            except Exception:
                pass

        # Fallback estimate based on file size
        estimated_duration = max(0.5, round(file_size / 32000.0, 2))
        return {
            'duration': estimated_duration,
            'sample_rate': 16000,
            'channels': 1,
            'file_size': file_size
        }

    @staticmethod
    def extract_features(filepath):
        """
        Extract MFCC and spectral acoustic features.
        Returns a dictionary of acoustic descriptors.
        """
        if not os.path.exists(filepath):
            return {
                'mfcc': [0.0] * 13,
                'spectral_centroid': 0.0,
                'rms_energy': 0.05,
                'duration': 1.0,
                'zero_crossing_rate': 0.0
            }

        if LIBROSA_AVAILABLE:
            try:
                y, sr = librosa.load(filepath, sr=16000)
                if len(y) == 0:
                    y = np.zeros(16000)

                mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
                mfcc_mean = [float(v) for v in np.mean(mfcc, axis=1)]

                centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
                rms = float(np.mean(librosa.feature.rms(y=y)))
                zcr = float(np.mean(librosa.feature.zero_crossing_rate(y=y)))
                duration = float(len(y) / sr)

                return {
                    'mfcc': mfcc_mean,
                    'spectral_centroid': centroid,
                    'rms_energy': rms,
                    'duration': duration,
                    'zero_crossing_rate': zcr
                }
            except Exception as e:
                print(f"[AudioService] Librosa feature extraction notice: {e}")

        # Lightweight fallback
        file_size = os.path.getsize(filepath)
        est_duration = max(0.5, min(10.0, file_size / 32000.0))
        return {
            'mfcc': [0.1] * 13,
            'spectral_centroid': 1500.0,
            'rms_energy': 0.08,
            'duration': est_duration,
            'zero_crossing_rate': 0.05
        }

    @staticmethod
    def transcribe_audio(filepath, language='english'):
        """
        Transcribe speech from audio file using Python SpeechRecognition as backend fallback.
        Returns recognized string or None.
        """
        if not SPEECH_REC_AVAILABLE or not os.path.exists(filepath):
            return None

        temp_wav = None
        try:
            recognizer = sr_lib.Recognizer()
            lang_code = 'hi-IN' if language.lower() == 'hindi' else 'en-US'

            # Convert to clean WAV using soundfile/librosa if not already a standard wav
            if LIBROSA_AVAILABLE and SOUNDFILE_AVAILABLE:
                y, sr = librosa.load(filepath, sr=16000)
                temp_fd, temp_wav = tempfile.mkstemp(suffix='.wav')
                os.close(temp_fd)
                sf.write(temp_wav, y, 16000)
                audio_target = temp_wav
            else:
                audio_target = filepath

            with sr_lib.AudioFile(audio_target) as source:
                audio_data = recognizer.record(source)
                transcript = recognizer.recognize_google(audio_data, language=lang_code)
                return transcript.strip()
        except Exception:
            return None
        finally:
            if temp_wav and os.path.exists(temp_wav):
                try:
                    os.remove(temp_wav)
                except OSError:
                    pass
