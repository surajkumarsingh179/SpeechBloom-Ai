"""
SpeechBloom AI - Flask Application Entry Point
Multilingual AI-powered speech therapy and pronunciation practice platform for children.
"""
import os
from flask import Flask
from config import Config
from database import init_db
from backend.services.ml_service import MLService


def create_app(config_class=Config):
    """Application factory for SpeechBloom AI."""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)

    # Initialize SQLite Database & register models
    init_db(app)

    # Ensure required directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['MODEL_PATH'], exist_ok=True)

    # Initialize Machine Learning Analysis Service
    ml_service = MLService()
    model_file = os.path.join(app.config['MODEL_PATH'], 'speechbloom_model.pkl')
    ml_service.load_model(model_file)
    app.config['ML_SERVICE'] = ml_service

    # Register blueprints
    from backend.routes.auth import auth_bp
    from backend.routes.profile import profile_bp
    from backend.routes.recording import recording_bp
    from backend.routes.exercise import exercise_bp
    from backend.routes.progress import progress_bp
    from backend.routes.dashboard import dashboard_bp
    from backend.routes.pages import pages_bp

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(profile_bp, url_prefix='/api')
    app.register_blueprint(recording_bp, url_prefix='/api')
    app.register_blueprint(exercise_bp, url_prefix='/api')
    app.register_blueprint(progress_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/api')
    app.register_blueprint(pages_bp, url_prefix='')

    @app.after_request
    def set_headers(response):
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

    return app


if __name__ == '__main__':
    app = create_app()
    print("=" * 60)
    print("🌸 SpeechBloom AI Server starting on http://127.0.0.1:5000")
    print("Mode: Demo Mode (Safe practice scoring - non-diagnostic)")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5000)
