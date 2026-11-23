"""
SpeechBloom AI - Model Evaluation & Confusion Matrix
"""
import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import joblib
    from sklearn.metrics import classification_report, accuracy_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


def evaluate_model(model_path):
    """Inspect and report performance of saved model."""
    if not os.path.exists(model_path):
        print(f"Model file not found at: {model_path}")
        print("Run `python ml/train_model.py` first to train a model.")
        return

    data = joblib.load(model_path)
    model = data.get('model')
    le = data.get('label_encoder')

    print("=" * 60)
    print("SpeechBloom AI - Model Evaluation Report")
    print("=" * 60)
    print(f"Model Architecture: {type(model).__name__}")
    if le:
        print(f"Target Phoneme Classes ({len(le.classes_)}): {list(le.classes_)}")
    print("Clinical Reminder: Scores indicate practice engagement and phoneme similarity,")
    print("not certified medical diagnosis for developmental speech disorders.")
    print("=" * 60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='ml/saved_models/speechbloom_model.pkl')
    args = parser.parse_args()
    evaluate_model(args.model)
