"""
SpeechBloom AI - Helper Utilities (Django-compatible)
"""
import os
import time
from werkzeug.utils import secure_filename


def allowed_audio_file(filename):
    """Check if the uploaded file has an allowed audio extension."""
    allowed = {'wav', 'mp3', 'ogg', 'webm', 'flac', 'm4a'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


def generate_filename(original_filename, child_id):
    """Generate a clean, unique filename for audio recordings."""
    ext       = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'wav'
    timestamp = int(time.time() * 1000)
    base      = secure_filename(original_filename.rsplit('.', 1)[0]) if '.' in original_filename else 'recording'
    return f"child_{child_id}_{timestamp}_{base}.{ext}"
