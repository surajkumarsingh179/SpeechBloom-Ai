"""
SpeechBloom AI - Inference & Prediction CLI
"""
import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.preprocessing import AudioPreprocessor
from ml.feature_extraction import FeatureExtractor
from backend.services.ml_service import MLService


def predict_audio(audio_path, language='english', phoneme='r'):
    """Analyze a single audio recording using ML pipeline."""
    if not os.path.exists(audio_path):
        print(f"Error: Audio file {audio_path} not found.")
        return

    clean_audio, sr = AudioPreprocessor.preprocess_pipeline(audio_path)
    features, _ = FeatureExtractor.extract_all_features(clean_audio, sr)

    ml = MLService(model_path='ml/saved_models/speechbloom_model.pkl')
    result = ml.analyze(features, language=language, target_phoneme=phoneme)

    print("=" * 50)
    print(f"🌸 SpeechBloom AI Prediction for: {audio_path}")
    print("=" * 50)
    print(f"Language:           {result['language']}")
    print(f"Target Phoneme:     {phoneme}")
    print(f"Observed Phoneme:   {result['observed_phoneme']}")
    print(f"Practice Score:     {result['score']}%")
    print(f"Encouragement:      {result['feedback']}")
    print(f"Mode:               {'Demo (Baseline)' if result['demo_mode'] else 'Trained Model'}")
    print("=" * 50)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="SpeechBloom AI Audio Predictor")
    parser.add_argument('--audio', required=True, help='Path to speech audio file')
    parser.add_argument('--lang', default='english', help='english or hindi')
    parser.add_argument('--phoneme', default='r', help='Target sound/phoneme')
    args = parser.parse_args()

    predict_audio(args.audio, args.lang, args.phoneme)
