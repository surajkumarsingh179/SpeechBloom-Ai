"""
SpeechBloom AI - Audio Recording & Speech Analysis Routes
"""
import os
from flask import Blueprint, request, jsonify, current_app
from backend.models.user import ChildProfile
from backend.models.recording import Recording, PracticeSession
from backend.services.audio_service import AudioService
from backend.services.gamification import GamificationService
from backend.utils.helpers import generate_filename
from database import db

recording_bp = Blueprint('recording', __name__)


@recording_bp.route('/recording', methods=['POST'])
def save_recording():
    if 'audio' not in request.files:
        return jsonify({'success': False, 'message': 'No audio file provided.'}), 400

    audio_file = request.files['audio']
    child_id = request.form.get('child_id')
    language = request.form.get('language', 'english').lower()
    target_word = request.form.get('target_word', '')
    target_phoneme = request.form.get('target_phoneme', '')
    observed_transcript = request.form.get('observed_transcript', '').strip()

    if not child_id:
        child = ChildProfile.query.first()
        child_id = child.id if child else 1
    else:
        child_id = int(child_id)

    upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], f"child_{child_id}")
    filename = generate_filename(audio_file.filename or 'speech.webm', child_id)
    filepath = AudioService.save_audio(audio_file.read(), filename, upload_folder)

    audio_info = AudioService.get_audio_info(filepath)

    # If client didn't supply transcript, attempt backend speech recognition
    if not observed_transcript:
        backend_transcription = AudioService.transcribe_audio(filepath, language)
        if backend_transcription:
            observed_transcript = backend_transcription

    recording = Recording(
        child_id=child_id,
        audio_path=filepath,
        language=language,
        target_word=target_word,
        target_phoneme=target_phoneme,
        observed_transcript=observed_transcript,
        duration=audio_info.get('duration', 1.0)
    )
    db.session.add(recording)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Recording saved successfully!',
        'recording_id': recording.id,
        'audio_path': filepath,
        'observed_transcript': observed_transcript,
        'duration': recording.duration
    }), 201


@recording_bp.route('/analyze', methods=['POST'])
def analyze_recording():
    data = request.get_json() or {}
    recording_id = data.get('recording_id')
    observed_transcript = data.get('observed_transcript')

    if not recording_id:
        return jsonify({'success': False, 'message': 'Recording ID required.'}), 400

    recording = db.session.get(Recording, recording_id)
    if not recording:
        return jsonify({'success': False, 'message': 'Recording record not found.'}), 404

    # Use transcript provided in request, or from recording, or attempt transcription
    if not observed_transcript:
        observed_transcript = recording.observed_transcript
    if not observed_transcript:
        observed_transcript = AudioService.transcribe_audio(recording.audio_path, recording.language)

    if observed_transcript and not recording.observed_transcript:
        recording.observed_transcript = observed_transcript
        db.session.commit()

    features = AudioService.extract_features(recording.audio_path)
    ml_service = current_app.config.get('ML_SERVICE')

    if ml_service:
        analysis = ml_service.analyze(
            features_dict=features,
            language=recording.language,
            target_word=recording.target_word,
            target_phoneme=recording.target_phoneme,
            observed_transcript=observed_transcript
        )
    else:
        analysis = {
            'score': 50.0,
            'feedback': 'Good effort! Let us try that sound again! 🌸',
            'confidence': 0.0,
            'observed_phoneme': recording.target_phoneme or 'clear',
            'observed_transcript': observed_transcript or '',
            'error_category': 'none',
            'demo_mode': True
        }

    score = float(analysis.get('score', 50.0))
    stars = GamificationService.calculate_stars(score)
    feedback_text = analysis.get('feedback', '')

    session_record = PracticeSession(
        child_id=recording.child_id,
        recording_id=recording.id,
        score=score,
        feedback=feedback_text,
        observed_phoneme=analysis.get('observed_phoneme', ''),
        error_category=analysis.get('error_category', 'none'),
        model_confidence=analysis.get('confidence', 0.0),
        demo_mode=analysis.get('demo_mode', True)
    )
    db.session.add(session_record)
    db.session.commit()

    new_badges = GamificationService.check_badges(recording.child_id, db.session)

    return jsonify({
        'success': True,
        'score': score,
        'feedback': feedback_text,
        'stars': stars,
        'confidence': analysis.get('confidence', 0.0),
        'observed_phoneme': analysis.get('observed_phoneme', ''),
        'observed_transcript': analysis.get('observed_transcript', ''),
        'target_word': recording.target_word,
        'error_category': analysis.get('error_category', 'none'),
        'demo_mode': analysis.get('demo_mode', True),
        'badges_earned': new_badges
    })
