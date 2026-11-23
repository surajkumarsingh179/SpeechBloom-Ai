"""
SpeechBloom AI - Parent & Therapist Dashboard APIs
"""
from flask import Blueprint, jsonify, current_app
from backend.models.user import ChildProfile, TherapistAssignment
from backend.models.recording import PracticeSession, Recording
from backend.utils.helpers import login_required, get_current_user

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard/parent', methods=['GET'])
@login_required
def parent_dashboard_data():
    user = get_current_user()
    children = user.children

    child_summaries = []
    all_child_ids = [c.id for c in children]
    total_sessions_all = 0
    total_seconds = 0

    for child in children:
        sessions = PracticeSession.query.filter_by(child_id=child.id).all()
        recs = Recording.query.filter_by(child_id=child.id).all()
        count = len(sessions)
        total_sessions_all += count
        dur = sum((r.duration or 0.0) for r in recs)
        total_seconds += dur

        avg = round(sum(s.score for s in sessions) / count, 1) if count > 0 else 0.0
        child_summaries.append({
            'child': child.to_dict(),
            'total_sessions': count,
            'average_score': avg,
            'practice_minutes': round(dur / 60.0, 1)
        })

    return jsonify({
        'success': True,
        'total_children': len(children),
        'total_sessions': total_sessions_all,
        'weekly_practice_minutes': round(total_seconds / 60.0, 1),
        'children_summary': child_summaries
    })


@dashboard_bp.route('/dashboard/therapist', methods=['GET'])
@login_required
def therapist_dashboard_data():
    user = get_current_user()
    assignments = TherapistAssignment.query.filter_by(therapist_id=user.id).all()

    assigned_children = []
    for a in assignments:
        child = a.child
        if child:
            sessions = PracticeSession.query.filter_by(child_id=child.id)\
                .order_by(PracticeSession.created_at.desc()).limit(10).all()
            assigned_children.append({
                'child': child.to_dict(),
                'parent_name': child.parent.name if child.parent else 'Unknown',
                'recent_sessions': [s.to_dict() for s in sessions]
            })

    return jsonify({
        'success': True,
        'therapist_name': user.name,
        'assigned_children': assigned_children
    })


@dashboard_bp.route('/model/status', methods=['GET'])
def get_model_status():
    ml_service = current_app.config.get('ML_SERVICE')
    if ml_service:
        return jsonify({'success': True, 'status': ml_service.get_status()})
    return jsonify({
        'success': True,
        'status': {
            'model_loaded': False,
            'model_type': 'Demo Mode (Baseline)',
            'demo_mode': True,
            'supported_languages': ['hindi', 'english']
        }
    })
