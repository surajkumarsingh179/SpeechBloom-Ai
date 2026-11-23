"""
SpeechBloom AI - Frontend Page Rendering Routes
"""
from flask import Blueprint, render_template, redirect, url_for, session
from backend.models.user import ChildProfile
from backend.utils.helpers import get_current_user

pages_bp = Blueprint('pages', __name__)


def get_template_context():
    """Build shared user context for Jinja2 templates."""
    user = get_current_user()
    children = []
    if user:
        children = [c.to_dict() for c in user.children]
    else:
        # Default fallback child for demo exploration
        demo_child = ChildProfile.query.first()
        if demo_child:
            children = [demo_child.to_dict()]

    return {
        'user': user.to_dict() if user else None,
        'children': children,
        'is_logged_in': user is not None,
        'role': user.role if user else None
    }


@pages_bp.route('/')
def index():
    return render_template('index.html', **get_template_context())


@pages_bp.route('/login')
def login():
    return render_template('login.html', **get_template_context())


@pages_bp.route('/register')
def register():
    return render_template('register.html', **get_template_context())


@pages_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('pages.index'))


@pages_bp.route('/dashboard')
def child_dashboard():
    return render_template('child_dashboard.html', **get_template_context())


@pages_bp.route('/profile')
def profile():
    return render_template('child_profile.html', **get_template_context())


@pages_bp.route('/practice')
def practice():
    return render_template('practice.html', **get_template_context())


@pages_bp.route('/recording')
def recording():
    return render_template('recording.html', **get_template_context())


@pages_bp.route('/games')
def games():
    return render_template('games.html', **get_template_context())


@pages_bp.route('/games/<game_type>')
def game_view(game_type):
    valid_games = ['repeat', 'explorer', 'matching', 'picture', 'phoneme', 'quest']
    if game_type in valid_games:
        return render_template(f"game_{game_type}.html", **get_template_context())
    return render_template('games.html', **get_template_context())


@pages_bp.route('/progress')
def progress():
    return render_template('progress.html', **get_template_context())


@pages_bp.route('/parent')
def parent_dashboard():
    return render_template('parent_dashboard.html', **get_template_context())


@pages_bp.route('/therapist')
def therapist_dashboard():
    return render_template('therapist_dashboard.html', **get_template_context())


@pages_bp.route('/about')
def about():
    return render_template('about.html', **get_template_context())


@pages_bp.route('/dataset-info')
def dataset_info():
    return render_template('dataset_info.html', **get_template_context())
