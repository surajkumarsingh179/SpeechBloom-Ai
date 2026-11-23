"""
SpeechBloom AI - Exercise & Gamification Models

Contains: Exercise, GameProgress, Badge
"""
from datetime import datetime
from database import db


class Exercise(db.Model):
    """A speech practice exercise (target word/phoneme with instructions)."""
    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(20), nullable=False)  # 'hindi' or 'english'
    category = db.Column(db.String(50))  # articulation, phoneme, word, sentence
    target_word = db.Column(db.String(100), nullable=False)
    target_phoneme = db.Column(db.String(50))
    difficulty = db.Column(db.Integer, default=1)  # 1 (easy) to 5 (hard)
    instructions = db.Column(db.Text)  # Directions shown to the child
    image_hint = db.Column(db.String(50))  # Emoji used as visual hint
    audio_ref_path = db.Column(db.String(500))  # Optional reference audio file

    # Relationships
    sessions = db.relationship('PracticeSession', backref='exercise', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'language': self.language,
            'category': self.category,
            'target_word': self.target_word,
            'target_phoneme': self.target_phoneme,
            'difficulty': self.difficulty,
            'instructions': self.instructions,
            'image_hint': self.image_hint,
            'audio_ref_path': self.audio_ref_path
        }


class GameProgress(db.Model):
    """Tracks a child's progress within a specific game type."""
    __tablename__ = 'game_progress'

    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child_profile.id'), nullable=False)
    game_type = db.Column(db.String(50), nullable=False)  # repeat, explorer, matching, picture, phoneme, quest
    score = db.Column(db.Integer, default=0)
    stars = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'child_id': self.child_id,
            'game_type': self.game_type,
            'score': self.score,
            'stars': self.stars,
            'level': self.level,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


class Badge(db.Model):
    """An achievement badge earned by a child."""
    __tablename__ = 'badge'

    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child_profile.id'), nullable=False)
    badge_type = db.Column(db.String(50), nullable=False)  # e.g. first_words, practice_pro, star_collector
    badge_name = db.Column(db.String(100), nullable=False)  # Display name
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'child_id': self.child_id,
            'badge_type': self.badge_type,
            'badge_name': self.badge_name,
            'earned_at': self.earned_at.isoformat() if self.earned_at else None
        }
