"""
SpeechBloom AI - Progress Tracking & Statistics Routes
"""
from datetime import datetime, timedelta
from flask import Blueprint, jsonify
from backend.models.recording import PracticeSession, Recording
from backend.models.exercise import Badge, Exercise
from database import db

progress_bp = Blueprint('progress', __name__)


@progress_bp.route('/progress/<int:child_id>', methods=['GET'])
def get_progress(child_id):
    sessions = PracticeSession.query.filter_by(child_id=child_id)\
        .order_by(PracticeSession.created_at.desc()).limit(50).all()

    total_sessions = len(sessions)
    scores = [s.score for s in sessions if s.score is not None]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0
    best_score = round(max(scores), 1) if scores else 0.0

    recordings = Recording.query.filter_by(child_id=child_id).all()
    distinct_words = len({r.target_word for r in recordings if r.target_word})
    total_duration = sum((r.duration or 0.0) for r in recordings)

    # Weekly data for Chart.js
    today = datetime.utcnow().date()
    weekly_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_sessions = [
            s for s in sessions
            if s.created_at and s.created_at.date() == day
        ]
        day_scores = [s.score for s in day_sessions if s.score is not None]
        weekly_data.append({
            'date': day.strftime('%b %d'),
            'sessions_count': len(day_sessions),
            'avg_score': round(sum(day_scores) / len(day_scores), 1) if day_scores else 0.0
        })

    # Streak calculation
    streak_days = 0
    cur_check = today
    while True:
        has_session = any(
            s.created_at and s.created_at.date() == cur_check
            for s in sessions
        )
        if has_session:
            streak_days += 1
            cur_check -= timedelta(days=1)
        else:
            break

    badges = Badge.query.filter_by(child_id=child_id).all()

    return jsonify({
        'success': True,
        'stats': {
            'total_sessions': total_sessions,
            'average_score': avg_score,
            'best_score': best_score,
            'words_practiced': distinct_words,
            'total_duration': round(total_duration, 1),
            'streak_days': streak_days
        },
        'sessions': [s.to_dict() for s in sessions],
        'weekly_data': weekly_data,
        'badges': [b.to_dict() for b in badges]
    })
