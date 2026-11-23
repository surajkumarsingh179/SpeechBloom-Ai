"""
SpeechBloom AI - Django Core Models
Models synchronized with Supabase PostgreSQL schema.
"""
import json
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class ParentUser(models.Model):
    """Parent or therapist user profile."""
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=256)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, default='parent')  # parent, therapist
    supabase_uid = models.CharField(max_length=64, blank=True, null=True)  # Supabase Auth UID
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'supabase_uid': self.supabase_uid
        }

    def __str__(self):
        return f"{self.name} ({self.email})"


class ChildProfile(models.Model):
    """Child learner profile registered by a parent."""
    parent = models.ForeignKey(ParentUser, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=5)
    languages = models.TextField(default='["english"]')  # JSON string
    avatar = models.CharField(max_length=50, default='🧒')
    supabase_id = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_languages(self):
        try:
            return json.loads(self.languages)
        except Exception:
            return ['english']

    def set_languages(self, lang_list):
        self.languages = json.dumps(lang_list)

    def to_dict(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'name': self.name,
            'age': self.age,
            'languages': self.get_languages(),
            'avatar': self.avatar
        }

    def __str__(self):
        return f"{self.name} (Child of {self.parent.name})"


class Recording(models.Model):
    """Audio speech recording by a child."""
    child = models.ForeignKey(ChildProfile, on_delete=models.CASCADE, related_name='recordings')
    audio_path = models.CharField(max_length=500)
    audio_url = models.CharField(max_length=500, blank=True, null=True)  # Supabase Storage public URL
    language = models.CharField(max_length=30, default='english')
    target_word = models.CharField(max_length=100, blank=True, null=True)
    target_phoneme = models.CharField(max_length=50, blank=True, null=True)
    observed_transcript = models.CharField(max_length=255, blank=True, null=True)
    duration = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            'id': self.id,
            'child_id': self.child_id,
            'audio_path': self.audio_path,
            'audio_url': self.audio_url or self.audio_path,
            'language': self.language,
            'target_word': self.target_word,
            'target_phoneme': self.target_phoneme,
            'observed_transcript': self.observed_transcript,
            'duration': self.duration,
            'created_at': self.created_at.isoformat()
        }


class PracticeSession(models.Model):
    """Result of speech practice evaluation."""
    child = models.ForeignKey(ChildProfile, on_delete=models.CASCADE, related_name='sessions')
    recording = models.ForeignKey(Recording, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.FloatField(default=80.0)
    feedback = models.TextField(blank=True)
    observed_phoneme = models.CharField(max_length=50, blank=True)
    error_category = models.CharField(max_length=50, default='none')  # none, substitution, distortion, omission
    model_confidence = models.FloatField(default=0.85)
    demo_mode = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            'id': self.id,
            'child_id': self.child_id,
            'score': self.score,
            'feedback': self.feedback,
            'observed_phoneme': self.observed_phoneme,
            'error_category': self.error_category,
            'created_at': self.created_at.isoformat()
        }


class Exercise(models.Model):
    """Speech practice target word and prompt."""
    language = models.CharField(max_length=20)
    category = models.CharField(max_length=50)  # articulation, phoneme, word, sentence
    target_word = models.CharField(max_length=100)
    target_phoneme = models.CharField(max_length=50, blank=True, null=True)
    difficulty = models.IntegerField(default=1)
    instructions = models.TextField(blank=True)
    image_hint = models.CharField(max_length=50, blank=True, null=True)

    def to_dict(self):
        return {
            'id': self.id,
            'language': self.language,
            'category': self.category,
            'target_word': self.target_word,
            'target_phoneme': self.target_phoneme,
            'difficulty': self.difficulty,
            'instructions': self.instructions,
            'image_hint': self.image_hint
        }


class Badge(models.Model):
    """Earned achievement badge."""
    child = models.ForeignKey(ChildProfile, on_delete=models.CASCADE, related_name='badges')
    badge_type = models.CharField(max_length=50)
    badge_name = models.CharField(max_length=100)
    earned_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            'id': self.id,
            'child_id': self.child_id,
            'badge_type': self.badge_type,
            'badge_name': self.badge_name,
            'earned_at': self.earned_at.isoformat()
        }
