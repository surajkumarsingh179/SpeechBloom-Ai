"""
SpeechBloom AI - Model Training Script
Trains baseline Random Forest phoneme classifier with speaker-separated splitting.
"""
import os
import sys
import argparse
import numpy as np

# Ensure root on python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.preprocessing import AudioPreprocessor
from ml.feature_extraction import FeatureExtractor

try:
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    from sklearn.model_selection import GroupShuffleSplit
    import joblib
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


def train_speech_model(annotation_csv, audio_dir, output_model_path):
    """
    Train a baseline Random Forest classifier on acoustic features.
    Splits by speaker_id to prevent speaker leakage.
    """
    if not SKLEARN_AVAILABLE:
        print("Error: pandas and scikit-learn are required to run training.")
        return

    if not os.path.exists(annotation_csv):
        print(f"Error: Annotations file not found: {annotation_csv}")
        return

    print(f"Loading annotations from {annotation_csv}...")
    df = pd.read_csv(annotation_csv)

    X_list = []
    y_list = []
    speakers = []

    print(f"Processing audio recordings from {audio_dir}...")
    for idx, row in df.iterrows():
        rel_path = row['audio_path']
        full_path = os.path.join(audio_dir, os.path.basename(rel_path))
        target_phoneme = str(row['target_phoneme'])
        speaker = str(row.get('speaker_id', f'spk_{idx}'))

        if os.path.exists(full_path):
            try:
                audio, sr = AudioPreprocessor.preprocess_pipeline(full_path)
                _, vector = FeatureExtractor.extract_all_features(audio, sr)
                X_list.append(vector)
                y_list.append(target_phoneme)
                speakers.append(speaker)
            except Exception as e:
                print(f"Skipping {full_path}: {e}")

    if len(X_list) < 5:
        print("Not enough audio samples found to train a robust model.")
        print("Creating placeholder baseline model for demonstration pipeline.")
        # Create synthetic demo model
        X_mock = np.random.randn(20, 31)
        y_mock = ['r', 's', 'l', 'k'] * 5
        le = LabelEncoder()
        y_enc = le.fit_transform(y_mock)
        clf = RandomForestClassifier(n_estimators=10, random_state=42)
        clf.fit(X_mock, y_enc)

        os.makedirs(os.path.dirname(output_model_path), exist_ok=True)
        joblib.dump({'model': clf, 'label_encoder': le}, output_model_path)
        print(f"✅ Demo baseline model saved to {output_model_path}")
        return

    X = np.array(X_list)
    le = LabelEncoder()
    y_enc = le.fit_transform(y_list)

    # Prevent speaker leakage: split by speaker
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_idx, test_idx = next(gss.split(X, y_enc, groups=speakers))

    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y_enc[train_idx], y_enc[test_idx]

    print(f"Training on {len(X_train)} samples across distinct speakers...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    train_acc = clf.score(X_train, y_train)
    test_acc = clf.score(X_test, y_test)
    print(f"Train Accuracy: {train_acc:.3f} | Test Accuracy: {test_acc:.3f}")

    os.makedirs(os.path.dirname(output_model_path), exist_ok=True)
    joblib.dump({'model': clf, 'label_encoder': le}, output_model_path)
    print(f"✅ Model successfully saved to {output_model_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="SpeechBloom AI - Model Trainer")
    parser.add_argument('--csv', default='datasets/annotations/speech_labels_template.csv', help='Path to annotation CSV')
    parser.add_argument('--audio', default='datasets/sample', help='Base audio directory')
    parser.add_argument('--out', default='ml/saved_models/speechbloom_model.pkl', help='Output model path')
    args = parser.parse_args()

    train_speech_model(args.csv, args.audio, args.out)
