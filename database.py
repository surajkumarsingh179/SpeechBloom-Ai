"""
SpeechBloom AI - Database Configuration

Uses Flask-SQLAlchemy for ORM with SQLite as the database engine.
"""
from flask_sqlalchemy import SQLAlchemy

# Global SQLAlchemy instance - shared across all models
db = SQLAlchemy()


def init_db(app):
    """
    Initialize the database with the Flask application.

    Args:
        app: Flask application instance with SQLALCHEMY_DATABASE_URI configured.

    This function:
    1. Binds the SQLAlchemy instance to the Flask app
    2. Imports all model modules so their tables are registered
    3. Creates all tables that don't yet exist
    """
    db.init_app(app)
    with app.app_context():
        # Import all models to register them with SQLAlchemy
        from backend.models import user, recording, exercise  # noqa: F401
        db.create_all()
