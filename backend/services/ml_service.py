"""
SpeechBloom AI - Machine Learning & Analysis Service
Handles speech evaluation, phonetic alignment, and pronunciation feedback scoring.
"""
import os
import random
from backend.services.phonetic_comparator import PhoneticComparator

try:
    import joblib
    JOBLIB_AVAILABLE = True
except ImportError:
    JOBLIB_AVAILABLE = False


class MLService:
    """Service handling pronunciation scoring and phoneme prediction."""

    def __init__(self, model_path=None):
        self.model = None
        self.model_type = None
        self.label_encoder = None
        self.demo_mode = True
        self.supported_languages = ['hindi', 'english']

        if model_path:
            self.load_model(model_path)

    def load_model(self, model_path):
        """Attempt to load a trained scikit-learn or joblib model file."""
        if not JOBLIB_AVAILABLE or not os.path.exists(model_path):
            self.demo_mode = True
            return False

        try:
            loaded_data = joblib.load(model_path)
            if isinstance(loaded_data, dict):
                self.model = loaded_data.get('model')
                self.label_encoder = loaded_data.get('label_encoder')
            else:
                self.model = loaded_data
            self.model_type = 'scikit-learn classifier'
            self.demo_mode = False
            return True
        except Exception as e:
            print(f"[MLService] Error loading model: {e}")
            self.demo_mode = True
            return False

    def analyze(self, features_dict, language='english', target_word='Sun', target_phoneme='s', observed_transcript=None):
        """
        Analyze speech audio features, transcript, and target word.
        Detects substitutions (e.g. 'lun' for 'sun'), omissions, and distortions.
        """
        # Run rigorous phonetic comparison against target sound and word
        evaluation = PhoneticComparator.evaluate_pronunciation(
            target_word=target_word or 'Word',
            target_phoneme=target_phoneme or '',
            observed_transcript=observed_transcript,
            acoustic_features=features_dict,
            language=language
        )

        score = evaluation['score']
        feedback = evaluation['feedback']
        observed_phoneme = evaluation['observed_phoneme']
        error_cat = evaluation['error_category']
        observed_transcript = evaluation['observed_transcript']
        is_match = evaluation['is_match']

        # If scikit-learn model is available, factor in acoustic classifier confidence
        confidence = 0.85 if is_match else 0.40
        if not self.demo_mode and self.model is not None:
            try:
                feature_vector = self._features_to_vector(features_dict)
                if hasattr(self.model, 'predict_proba'):
                    proba = self.model.predict_proba([feature_vector])[0]
                    confidence = float(max(proba))
            except Exception:
                pass

        return {
            'score': score,
            'feedback': feedback,
            'confidence': round(confidence, 2),
            'observed_phoneme': observed_phoneme,
            'observed_transcript': observed_transcript,
            'target_word': target_word,
            'error_category': error_cat,
            'demo_mode': self.demo_mode,
            'language': language
        }

    def _features_to_vector(self, features_dict):
        mfcc = features_dict.get('mfcc', [0.0] * 13)
        centroid = float(features_dict.get('spectral_centroid', 0.0))
        rms = float(features_dict.get('rms_energy', 0.0))
        duration = float(features_dict.get('duration', 0.0))
        zcr = float(features_dict.get('zero_crossing_rate', 0.0))
        return list(mfcc[:13]) + [centroid, rms, duration, zcr]

    def get_status(self):
        return {
            'model_loaded': self.model is not None,
            'model_type': self.model_type if self.model else 'Phonetic Alignment & Baseline Acoustic Engine',
            'demo_mode': self.demo_mode,
            'supported_languages': self.supported_languages
        }
