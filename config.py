"""
SpeechBloom AI - Application Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration loaded from environment variables with sensible defaults."""

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'speechbloom-dev-secret-key-change-in-production')

    # Paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI',
        'sqlite:///' + os.path.join(BASE_DIR, 'speechbloom.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, os.environ.get('UPLOAD_FOLDER', 'uploads'))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload

    # ML Model
    MODEL_PATH = os.path.join(BASE_DIR, os.environ.get('MODEL_PATH', 'ml/saved_models'))
    DEMO_MODE = os.environ.get('DEMO_MODE', 'true').lower() == 'true'

    # Supported languages
    SUPPORTED_LANGUAGES = ['hindi', 'english']

    # Audio settings
    ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'ogg', 'webm', 'flac'}
    TARGET_SAMPLE_RATE = 16000
