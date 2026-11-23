"""
SpeechBloom AI - Routes Package
Exports all Blueprint modules.
"""
from backend.routes.auth import auth_bp
from backend.routes.profile import profile_bp
from backend.routes.recording import recording_bp
from backend.routes.exercise import exercise_bp
from backend.routes.progress import progress_bp
from backend.routes.dashboard import dashboard_bp
from backend.routes.pages import pages_bp

__all__ = [
    'auth_bp',
    'profile_bp',
    'recording_bp',
    'exercise_bp',
    'progress_bp',
    'dashboard_bp',
    'pages_bp'
]
