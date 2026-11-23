"""
SpeechBloom AI - Recording Models

Contains: Recording, PracticeSession
"""
from datetime import datetime
from database import db


class Recording(db.Model):
    """An audio recording made by a child during practice."""
    __tablename__ = 'recording'

    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child_profile.id'), nullable=False)
    audio_path = db.Column(db.String(500), nullable=False)
    language = db.Column(db.String(20), nullable=False)  # 'hindi' or 'english'
    target_word = db.Column(db.String(100))
    target_phoneme = db.Column(db.String(50))
    observed_transcript = db.Column(db.String(255))
    duration = db.Column(db.Float)  # Duration in seconds
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    sessions = db.relationship('PracticeSession', backref='recording', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'child_id': self.child_id,
            'audio_path': self.audio_path,
            'language': self.language,
            'target_word': self.target_word,
            'target_phoneme': self.target_phoneme,
            'observed_transcript': self.observed_transcript,
            'duration': self.duration,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class PracticeSession(db.Model):
    """
    Result of analyzing a recording against a target.

    Important: When demo_mode=True, the score and feedback are generated
    by a demonstration algorithm, NOT by a validated clinical model.
    Demo results should never be treated as clinical assessments.
    """
    __tablename__ = 'practice_session'

    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child_profile.id'), nullable=False)
    recording_id = db.Column(db.Integer, db.ForeignKey('recording.id'), nullable=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=True)
    score = db.Column(db.Float)  # 0-100 practice score
    feedback = db.Column(db.Text)  # Encouraging feedback message
    observed_phoneme = db.Column(db.String(50))  # What the model/demo detected
    error_category = db.Column(db.String(50))  # none, substitution, omission, distortion
    model_confidence = db.Column(db.Float)  # 0.0-1.0 confidence (0.0 for demo mode)
    demo_mode = db.Column(db.Boolean, default=True)  # True = demo, not clinically validated
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'child_id': self.child_id,
            'recording_id': self.recording_id,
            'exercise_id': self.exercise_id,
            'score': self.score,
            'feedback': self.feedback,
            'observed_phoneme': self.observed_phoneme,
            'error_category': self.error_category,
            'model_confidence': self.model_confidence,
            'demo_mode': self.demo_mode,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
