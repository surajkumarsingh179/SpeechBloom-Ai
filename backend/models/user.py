"""
SpeechBloom AI - User Models

Contains: User, ChildProfile, TherapistAssignment
"""
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database import db


class User(db.Model):
    """Parent or therapist account."""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='parent')  # parent, therapist, admin
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    children = db.relationship('ChildProfile', backref='parent', lazy=True,
                               foreign_keys='ChildProfile.parent_id')

    def set_password(self, password):
        """Hash and store the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify a password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ChildProfile(db.Model):
    """Profile for a child using the platform."""
    __tablename__ = 'child_profile'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    languages = db.Column(db.Text, default='["english"]')  # JSON array of language strings
    avatar = db.Column(db.String(50), default='🧒')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    recordings = db.relationship('Recording', backref='child', lazy=True)
    practice_sessions = db.relationship('PracticeSession', backref='child', lazy=True)
    game_progress = db.relationship('GameProgress', backref='child', lazy=True)
    badges = db.relationship('Badge', backref='child', lazy=True)

    def get_languages(self):
        """Parse the JSON languages field into a Python list."""
        try:
            return json.loads(self.languages) if self.languages else ['english']
        except (json.JSONDecodeError, TypeError):
            return ['english']

    def set_languages(self, langs_list):
        """Store a list of languages as a JSON string."""
        self.languages = json.dumps(langs_list)

    def to_dict(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'name': self.name,
            'age': self.age,
            'languages': self.get_languages(),
            'avatar': self.avatar,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class TherapistAssignment(db.Model):
    """Links a therapist to a child they are working with."""
    __tablename__ = 'therapist_assignment'

    id = db.Column(db.Integer, primary_key=True)
    therapist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey('child_profile.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    therapist = db.relationship('User', foreign_keys=[therapist_id])
    child = db.relationship('ChildProfile', foreign_keys=[child_id])

    def to_dict(self):
        return {
            'id': self.id,
            'therapist_id': self.therapist_id,
            'child_id': self.child_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
