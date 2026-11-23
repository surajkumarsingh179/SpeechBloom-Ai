"""
SpeechBloom AI - Profile Management Routes
"""
from flask import Blueprint, request, jsonify
from backend.models.user import ChildProfile
from backend.models.recording import PracticeSession
from backend.models.exercise import GameProgress
from backend.utils.helpers import login_required, get_current_user
from database import db

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    user = get_current_user()
    children = [c.to_dict() for c in user.children]
    return jsonify({
        'success': True,
        'user': user.to_dict(),
        'children': children
    })


@profile_bp.route('/children', methods=['GET'])
@login_required
def list_children():
    user = get_current_user()
    return jsonify({
        'success': True,
        'children': [c.to_dict() for c in user.children]
    })


@profile_bp.route('/children', methods=['POST'])
@login_required
def create_child():
    user = get_current_user()
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    age = data.get('age', 5)
    languages = data.get('languages', ['english'])
    avatar = data.get('avatar', '🧒')

    if not name:
        return jsonify({'success': False, 'message': 'Child name is required.'}), 400

    child = ChildProfile(
        parent_id=user.id,
        name=name,
        age=int(age),
        avatar=avatar
    )
    child.set_languages(languages)
    db.session.add(child)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Child profile added!',
        'child': child.to_dict()
    }), 201


@profile_bp.route('/children/<int:child_id>', methods=['GET'])
@login_required
def get_child_details(child_id):
    child = db.session.get(ChildProfile, child_id)
    if not child:
        return jsonify({'success': False, 'message': 'Child not found.'}), 404

    sessions = PracticeSession.query.filter_by(child_id=child.id).all()
    total_sessions = len(sessions)
    avg_score = round(sum(s.score for s in sessions) / total_sessions, 1) if total_sessions > 0 else 0.0

    games = GameProgress.query.filter_by(child_id=child.id).all()
    total_stars = sum(g.stars for g in games)

    details = child.to_dict()
    details.update({
        'total_sessions': total_sessions,
        'average_score': avg_score,
        'total_stars': total_stars
    })

    return jsonify({'success': True, 'child': details})
