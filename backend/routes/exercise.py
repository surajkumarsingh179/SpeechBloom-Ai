"""
SpeechBloom AI - Exercise & Game Routes
"""
from flask import Blueprint, request, jsonify
from backend.models.exercise import Exercise, GameProgress, Badge
from backend.models.recording import PracticeSession
from backend.services.gamification import GamificationService
from database import db

exercise_bp = Blueprint('exercise', __name__)


@exercise_bp.route('/exercises', methods=['GET'])
def list_exercises():
    language = request.args.get('language', '').lower()
    category = request.args.get('category', '').lower()
    difficulty = request.args.get('difficulty')

    query = Exercise.query
    if language:
        query = query.filter_by(language=language)
    if category:
        query = query.filter_by(category=category)
    if difficulty:
        try:
            query = query.filter_by(difficulty=int(difficulty))
        except ValueError:
            pass

    exercises = query.limit(60).all()
    return jsonify({
        'success': True,
        'count': len(exercises),
        'exercises': [e.to_dict() for e in exercises]
    })


@exercise_bp.route('/exercises/complete', methods=['POST'])
def complete_exercise():
    data = request.get_json() or {}
    child_id = data.get('child_id', 1)
    exercise_id = data.get('exercise_id')
    score = float(data.get('score', 85.0))
    feedback = data.get('feedback', 'Keep practicing!')

    session_record = PracticeSession(
        child_id=int(child_id),
        exercise_id=int(exercise_id) if exercise_id else None,
        score=score,
        feedback=feedback,
        demo_mode=True
    )
    db.session.add(session_record)
    db.session.commit()

    stars = GamificationService.calculate_stars(score)
    encouragement = GamificationService.get_encouragement(score)
    badges = GamificationService.check_badges(int(child_id), db.session)

    return jsonify({
        'success': True,
        'session': session_record.to_dict(),
        'stars': stars,
        'encouragement': encouragement,
        'badges_earned': badges
    })


@exercise_bp.route('/games/progress/<int:child_id>', methods=['GET'])
def get_game_progress(child_id):
    progress = GameProgress.query.filter_by(child_id=child_id).all()
    badges = Badge.query.filter_by(child_id=child_id).all()

    total_stars = sum(p.stars for p in progress)
    level = GamificationService.get_level(total_stars)

    return jsonify({
        'success': True,
        'progress': [p.to_dict() for p in progress],
        'badges': [b.to_dict() for b in badges],
        'total_stars': total_stars,
        'level': level
    })


@exercise_bp.route('/games/save', methods=['POST'])
def save_game_progress():
    data = request.get_json() or {}
    child_id = int(data.get('child_id', 1))
    game_type = data.get('game_type', 'repeat')
    score = int(data.get('score', 0))
    stars = int(data.get('stars', 0))
    level = int(data.get('level', 1))

    record = GameProgress(
        child_id=child_id,
        game_type=game_type,
        score=score,
        stars=stars,
        level=level
    )
    db.session.add(record)
    db.session.commit()

    new_badges = GamificationService.check_badges(child_id, db.session)

    return jsonify({
        'success': True,
        'message': 'Game progress saved!',
        'progress': record.to_dict(),
        'badges_earned': new_badges
    })


@exercise_bp.route('/games/quest/<int:child_id>', methods=['GET'])
def get_quest(child_id):
    language = request.args.get('language', 'english').lower()
    quest = GamificationService.get_daily_quest(child_id, language)
    return jsonify({
        'success': True,
        'quest': quest
    })
