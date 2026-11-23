"""
SpeechBloom AI - Django Core Views & APIs
"""
import os
import json
from datetime import datetime, timedelta, timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from core.models import ParentUser, ChildProfile, Recording, PracticeSession, Exercise, Badge
from backend.services.supabase_service import supabase_service
from backend.services.audio_service import AudioService
from backend.services.ml_service import MLService
from backend.services.gamification import GamificationService
from backend.utils.helpers import generate_filename

ml_engine = MLService()


# ── Helpers ──────────────────────────────────────────────────
def _require_login(request):
    """Return (user_id, error_response) pair. error_response is None if logged in."""
    uid = request.session.get('user_id')
    if not uid:
        return None, JsonResponse({'success': False, 'message': 'Authentication required.'}, status=401)
    return uid, None


# ── PAGE VIEWS ───────────────────────────────────────────────
def index_view(request):
    return render(request, 'index.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def logout_view(request):
    request.session.flush()
    return redirect('/')

def child_profile_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/login/')
    children = ChildProfile.objects.filter(parent_id=user_id)
    return render(request, 'child_profile.html', {'children': [c.to_dict() for c in children]})

def child_dashboard_view(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'child_dashboard.html')

def practice_view(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'practice.html')

def recording_view(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'recording.html')

def games_hub_view(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'games.html')

def game_detail_view(request, game_type):
    if not request.session.get('user_id'):
        return redirect('/login/')
    clean_type = game_type.replace('-', '_')
    valid_games = ['repeat', 'explorer', 'matching', 'picture', 'phoneme', 'quest', 'cat_puzzle']
    if clean_type in valid_games:
        return render(request, f"game_{clean_type}.html")
    return render(request, 'games.html')

def progress_view(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'progress.html')

def parent_dashboard_view(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'parent_dashboard.html')

def therapist_dashboard_view(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    return render(request, 'therapist_dashboard.html')

def about_view(request):
    return render(request, 'about.html')

def dataset_info_view(request):
    return render(request, 'dataset_info.html')


# ── AUTH APIs ────────────────────────────────────────────────
@csrf_exempt
def api_register(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    email    = data.get('email', '').strip().lower()
    password = data.get('password', '')
    name     = data.get('name', '').strip()
    role     = data.get('role', 'parent').lower()

    if not email or not password or not name:
        return JsonResponse({'success': False, 'message': 'Name, email, and password are required.'}, status=400)
    if len(password) < 6:
        return JsonResponse({'success': False, 'message': 'Password must be at least 6 characters.'}, status=400)

    # Supabase Auth registration
    supabase_uid = None
    sb_res = supabase_service.sign_up_parent(email, password, name, role)
    if sb_res and sb_res.get('success'):
        supabase_uid = sb_res['user']['id']
    elif sb_res and not sb_res.get('success'):
        print(f"[Supabase Notice] {sb_res.get('message')}")

    if ParentUser.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'message': 'Account already exists. Please sign in.'}, status=409)

    user = ParentUser(email=email, name=name, role=role, supabase_uid=supabase_uid)
    user.set_password(password)
    user.save()
    request.session['user_id'] = user.id

    return JsonResponse({
        'success': True,
        'message': 'Account created! Add your child\'s profile to begin.',
        'user': user.to_dict(),
        'redirect_url': '/profile/'
    }, status=201)


@csrf_exempt
def api_login(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    email    = data.get('email', '').strip().lower()
    password = data.get('password', '')

    # 1. Try Supabase Auth
    sb_res = supabase_service.sign_in_parent(email, password)
    if sb_res and sb_res.get('success'):
        sb_user = sb_res['user']
        user, _ = ParentUser.objects.get_or_create(
            email=email,
            defaults={
                'name': sb_user.get('name', email.split('@')[0]),
                'role': sb_user.get('role', 'parent'),
                'supabase_uid': sb_user.get('id', '')
            }
        )
        request.session['user_id'] = user.id
        has_children = user.children.exists()
        return JsonResponse({
            'success': True,
            'user': user.to_dict(),
            'redirect_url': '/parent/' if has_children else '/profile/'
        })

    # 2. Local fallback
    try:
        user = ParentUser.objects.get(email=email)
        if user.check_password(password):
            request.session['user_id'] = user.id
            has_children = user.children.exists()
            return JsonResponse({
                'success': True,
                'user': user.to_dict(),
                'redirect_url': '/parent/' if has_children else '/profile/'
            })
    except ParentUser.DoesNotExist:
        pass

    return JsonResponse({'success': False, 'message': 'Invalid email or password.'}, status=401)


# ── CHILD PROFILE APIs ───────────────────────────────────────
@csrf_exempt
def api_children(request):
    user_id, err = _require_login(request)
    if err:
        return err

    if request.method == 'GET':
        children = ChildProfile.objects.filter(parent_id=user_id)
        return JsonResponse({'success': True, 'children': [c.to_dict() for c in children]})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception:
            data = request.POST

        name      = data.get('name', '').strip()
        age       = data.get('age', 5)
        languages = data.get('languages', ['english'])
        avatar    = data.get('avatar', '🧒')

        if not name:
            return JsonResponse({'success': False, 'message': 'Child name is required'}, status=400)

        parent = ParentUser.objects.filter(id=user_id).first()
        if not parent:
            return JsonResponse({'success': False, 'message': 'Parent account not found.'}, status=404)

        # Sync to Supabase
        sb_child = supabase_service.create_child_profile(
            parent_id=user_id, name=name, age=age, languages=languages, avatar=avatar
        )
        sb_id = sb_child.get('child', {}).get('id') if sb_child and sb_child.get('success') else None

        # Save locally
        child = ChildProfile(parent=parent, name=name, age=int(age), avatar=avatar, supabase_id=sb_id)
        child.set_languages(languages)
        child.save()

        return JsonResponse({
            'success': True,
            'message': 'Child profile created!',
            'child': child.to_dict()
        }, status=201)

    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)


@csrf_exempt
def api_parent_dashboard(request):
    user_id, err = _require_login(request)
    if err:
        return err

    children              = ChildProfile.objects.filter(parent_id=user_id)
    child_summaries       = []
    total_family_sessions = 0
    total_practice_secs   = 0
    detailed_reports      = []

    for child in children:
        sessions = PracticeSession.objects.filter(child_id=child.id).order_by('-created_at')
        count    = sessions.count()
        total_family_sessions += count

        scores    = [s.score for s in sessions]
        avg_score = round(sum(scores) / count, 1) if count > 0 else 0.0

        recs = Recording.objects.filter(child_id=child.id)
        dur  = sum(r.duration for r in recs)
        total_practice_secs += dur

        substitutions     = sessions.filter(error_category='substitution').count()
        distortions       = sessions.filter(error_category='distortion').count()
        clean_articu      = sessions.filter(error_category='none').count()

        child_summaries.append({
            'child':              child.to_dict(),
            'total_sessions':     count,
            'average_score':      avg_score,
            'practice_minutes':   round(dur / 60.0, 1),
            'clean_count':        clean_articu,
            'substitution_count': substitutions,
            'distortion_count':   distortions,
        })
        detailed_reports.append({
            'child_name':     child.name,
            'age':            child.age,
            'avatar':         child.avatar,
            'avg_score':      avg_score,
            'total_sessions': count,
            'recent_practice': [s.to_dict() for s in sessions[:5]],
        })

    return JsonResponse({
        'success':                 True,
        'supabase_connected':      supabase_service.is_connected,
        'total_children':          children.count(),
        'total_sessions':          total_family_sessions,
        'weekly_practice_minutes': round(total_practice_secs / 60.0, 1),
        'children_summary':        child_summaries,
        'detailed_reports':        detailed_reports,
    })


# ── RECORDING & ANALYSIS APIs ────────────────────────────────
@csrf_exempt
def api_recording(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

    user_id = request.session.get('user_id')

    audio_file = request.FILES.get('audio')
    if not audio_file:
        return JsonResponse({'success': False, 'message': 'No audio file uploaded.'}, status=400)

    child_id            = request.POST.get('child_id')
    language            = request.POST.get('language', 'english').lower()
    target_word         = request.POST.get('target_word', '')
    target_phoneme      = request.POST.get('target_phoneme', '')
    observed_transcript = request.POST.get('observed_transcript', '').strip()

    # Validate child_id belongs to this user (security)
    if child_id:
        try:
            child_id  = int(child_id)
            child_obj = ChildProfile.objects.get(id=child_id)
            # If logged in, verify ownership
            if user_id and str(child_obj.parent_id) != str(user_id):
                return JsonResponse({'success': False, 'message': 'Access denied.'}, status=403)
        except (ChildProfile.DoesNotExist, ValueError):
            child_obj = None
    else:
        child_obj = None

    # Fallback: attach to first child of this user (never to a stranger's child)
    if not child_obj:
        if user_id:
            child_obj = ChildProfile.objects.filter(parent_id=user_id).first()
        if not child_obj:
            default_parent, _ = ParentUser.objects.get_or_create(
                email="demo@speechbloom.ai",
                defaults={'name': 'Demo Parent'}
            )
            if not default_parent.password_hash:
                default_parent.set_password('speechbloom_demo')
                default_parent.save()
            child_obj = ChildProfile.objects.filter(parent=default_parent).first()
            if not child_obj:
                child_obj = ChildProfile.objects.create(parent=default_parent, name="Demo Child", age=6)

    child_id = child_obj.id

    upload_dir  = os.path.join('uploads', f"child_{child_id}")
    filename    = generate_filename(audio_file.name or 'speech.wav', child_id)
    audio_bytes = audio_file.read()
    filepath    = AudioService.save_audio(audio_bytes, filename, upload_dir)
    audio_info  = AudioService.get_audio_info(filepath)

    supabase_audio_url = supabase_service.upload_recording_audio(
        file_bytes=audio_bytes,
        filename=f"child_{child_id}/{filename}",
        content_type="audio/wav"
    )

    if not observed_transcript:
        backend_heard = AudioService.transcribe_audio(filepath, language)
        if backend_heard:
            observed_transcript = backend_heard

    recording = Recording.objects.create(
        child=child_obj,
        audio_path=filepath,
        audio_url=supabase_audio_url or filepath,
        language=language,
        target_word=target_word,
        target_phoneme=target_phoneme,
        observed_transcript=observed_transcript,
        duration=audio_info.get('duration', 1.0)
    )

    return JsonResponse({
        'success':              True,
        'recording_id':         recording.id,
        'audio_path':           filepath,
        'audio_url':            recording.audio_url,
        'observed_transcript':  observed_transcript,
        'duration':             recording.duration,
    }, status=201)


@csrf_exempt
def api_analyze(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    recording_id        = data.get('recording_id')
    observed_transcript = data.get('observed_transcript', '').strip()

    if not recording_id:
        return JsonResponse({'success': False, 'message': 'Recording ID required'}, status=400)

    try:
        recording = Recording.objects.get(id=recording_id)
    except Recording.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Recording not found'}, status=404)

    if not observed_transcript:
        observed_transcript = recording.observed_transcript or AudioService.transcribe_audio(
            recording.audio_path, recording.language
        )

    if observed_transcript and not recording.observed_transcript:
        recording.observed_transcript = observed_transcript
        recording.save()

    features = AudioService.extract_features(recording.audio_path)
    analysis = ml_engine.analyze(
        features_dict=features,
        language=recording.language,
        target_word=recording.target_word,
        target_phoneme=recording.target_phoneme,
        observed_transcript=observed_transcript
    )

    score       = float(analysis['score'])
    stars       = GamificationService.calculate_stars(score)
    feedback    = analysis['feedback']
    error_cat   = analysis['error_category']
    observed_ph = analysis['observed_phoneme']

    PracticeSession.objects.create(
        child=recording.child,
        recording=recording,
        score=score,
        feedback=feedback,
        observed_phoneme=observed_ph,
        error_category=error_cat,
        model_confidence=analysis['confidence']
    )

    supabase_service.log_practice_session(
        child_id=recording.child_id,
        recording_url=recording.audio_url,
        target_word=recording.target_word,
        target_phoneme=recording.target_phoneme,
        observed_phoneme=observed_ph,
        score=score,
        feedback=feedback,
        error_category=error_cat
    )

    return JsonResponse({
        'success':              True,
        'score':                score,
        'feedback':             feedback,
        'stars':                stars,
        'confidence':           analysis['confidence'],
        'observed_phoneme':     observed_ph,
        'observed_transcript':  analysis['observed_transcript'],
        'target_word':          recording.target_word,
        'error_category':       error_cat,
        'audio_url':            recording.audio_url,
        'supabase_synced':      supabase_service.is_connected,
    })


# ── EXERCISES & PROGRESS APIs ────────────────────────────────
def api_exercises(request):
    lang = request.GET.get('language', '').lower()
    cat  = request.GET.get('category', '').lower()
    diff = request.GET.get('difficulty')

    qs = Exercise.objects.all()
    if lang:
        qs = qs.filter(language=lang)
    if cat:
        qs = qs.filter(category=cat)
    if diff:
        try:
            qs = qs.filter(difficulty=int(diff))
        except ValueError:
            pass

    return JsonResponse({'success': True, 'count': qs.count(), 'exercises': [e.to_dict() for e in qs[:60]]})


def api_progress(request, child_id):
    sessions = PracticeSession.objects.filter(child_id=child_id).order_by('-created_at')[:50]
    count    = sessions.count()
    scores   = [s.score for s in sessions]
    avg_score = round(sum(scores) / count, 1) if count > 0 else 0.0

    # Use timezone-aware datetime (Python 3.12 compatible)
    today = datetime.now(timezone.utc).date()

    # ── Correct streak: consecutive days ending today or yesterday
    dates_active = set(s.created_at.date() for s in sessions)
    streak = 0
    if today in dates_active:
        check_day = today
    elif (today - timedelta(days=1)) in dates_active:
        check_day = today - timedelta(days=1)
    else:
        check_day = None
    if check_day:
        while check_day in dates_active:
            streak   += 1
            check_day -= timedelta(days=1)
    weekly_data = []
    for i in range(6, -1, -1):
        day         = today - timedelta(days=i)
        day_sessions = [s for s in sessions if s.created_at.date() == day]
        day_scores  = [s.score for s in day_sessions]
        weekly_data.append({
            'date':           day.strftime('%b %d'),
            'sessions_count': len(day_sessions),
            'avg_score':      round(sum(day_scores) / len(day_scores), 1) if day_scores else 0.0,
        })

    return JsonResponse({
        'success': True,
        'stats': {
            'total_sessions':  count,
            'average_score':   avg_score,
            'streak_days':     streak,
        },
        'sessions':    [s.to_dict() for s in sessions],
        'weekly_data': weekly_data,
    })


def api_game_progress(request, child_id):
    sessions    = PracticeSession.objects.filter(child_id=child_id)
    total_stars = sum(GamificationService.calculate_stars(s.score) for s in sessions)
    level       = GamificationService.get_level(total_stars)
    return JsonResponse({'success': True, 'total_stars': total_stars, 'level': level})


@csrf_exempt
def api_game_save(request):
    """Save a game score (called from games.js saveGameScore)."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

    user_id = request.session.get('user_id')

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = {}

    child_id  = data.get('child_id') or (request.session.get('user_id'))
    score     = float(data.get('score', 0))
    stars     = int(data.get('stars', 0))
    game_type = data.get('game_type', 'unknown')

    # Lightweight — just acknowledge; full session logging uses api_analyze
    return JsonResponse({'success': True, 'stars': stars, 'score': score, 'game_type': game_type})


def api_model_status(request):
    return JsonResponse({'success': True, 'status': ml_engine.get_status()})


# ── UNIQUE WORDS PRACTICED ────────────────────────────────
def api_unique_words(request, child_id):
    """Count distinct target words this child has successfully practiced."""
    # Pull all sessions with a non-empty target_word via their recording
    session_ids = PracticeSession.objects.filter(child_id=child_id).values_list('recording_id', flat=True)
    words_tried = (
        Recording.objects
        .filter(id__in=session_ids, target_word__isnull=False)
        .exclude(target_word='')
        .values_list('target_word', flat=True)
        .distinct()
    )
    unique_count = words_tried.count()
    return JsonResponse({'success': True, 'unique_words': unique_count, 'words': list(words_tried)})


# ── DAILY QUEST ───────────────────────────────────────────
# Expanded pool across diverse vocabulary, phonemes, and sentences
_QUEST_POOL = [
    # English Words
    {'word': 'Sun',        'phoneme': 's',   'lang': 'english', 'emoji': '☀️', 'type': 'word'},
    {'word': 'Ball',       'phoneme': 'b',   'lang': 'english', 'emoji': '⚽', 'type': 'word'},
    {'word': 'Cat',        'phoneme': 'k',   'lang': 'english', 'emoji': '🐱', 'type': 'word'},
    {'word': 'Dog',        'phoneme': 'd',   'lang': 'english', 'emoji': '🐶', 'type': 'word'},
    {'word': 'Fish',       'phoneme': 'f',   'lang': 'english', 'emoji': '🐟', 'type': 'word'},
    {'word': 'Red',        'phoneme': 'r',   'lang': 'english', 'emoji': '🔴', 'type': 'word'},
    {'word': 'Ship',       'phoneme': 'sh',  'lang': 'english', 'emoji': '🚢', 'type': 'word'},
    {'word': 'Lion',       'phoneme': 'l',   'lang': 'english', 'emoji': '🦁', 'type': 'word'},
    {'word': 'Apple',      'phoneme': 'æ',   'lang': 'english', 'emoji': '🍎', 'type': 'word'},
    {'word': 'Tree',       'phoneme': 'tr',  'lang': 'english', 'emoji': '🌳', 'type': 'word'},
    {'word': 'Flower',     'phoneme': 'fl',  'lang': 'english', 'emoji': '🌸', 'type': 'word'},
    {'word': 'Rabbit',     'phoneme': 'r',   'lang': 'english', 'emoji': '🐰', 'type': 'word'},
    {'word': 'Elephant',   'phoneme': 'e',   'lang': 'english', 'emoji': '🐘', 'type': 'word'},
    {'word': 'Butterfly',  'phoneme': 'b',   'lang': 'english', 'emoji': '🦋', 'type': 'word'},
    {'word': 'Rainbow',    'phoneme': 'r',   'lang': 'english', 'emoji': '🌈', 'type': 'word'},
    {'word': 'Star',       'phoneme': 'st',  'lang': 'english', 'emoji': '⭐', 'type': 'word'},
    {'word': 'Clock',      'phoneme': 'kl',  'lang': 'english', 'emoji': '🕐', 'type': 'word'},
    {'word': 'Frog',       'phoneme': 'fr',  'lang': 'english', 'emoji': '🐸', 'type': 'word'},
    {'word': 'Spoon',      'phoneme': 'sp',  'lang': 'english', 'emoji': '🥄', 'type': 'word'},
    {'word': 'Mountain',   'phoneme': 'm',   'lang': 'english', 'emoji': '🏔️', 'type': 'word'},
    {'word': 'Strawberry', 'phoneme': 'str', 'lang': 'english', 'emoji': '🍓', 'type': 'word'},
    {'word': 'Water',      'phoneme': 'w',   'lang': 'english', 'emoji': '💧', 'type': 'word'},
    {'word': 'Train',      'phoneme': 'tr',  'lang': 'english', 'emoji': '🚂', 'type': 'word'},
    {'word': 'Bird',       'phoneme': 'b',   'lang': 'english', 'emoji': '🐦', 'type': 'word'},
    {'word': 'House',      'phoneme': 'h',   'lang': 'english', 'emoji': '🏠', 'type': 'word'},
    {'word': 'Moon',       'phoneme': 'm',   'lang': 'english', 'emoji': '🌙', 'type': 'word'},
    {'word': 'Pencil',     'phoneme': 'p',   'lang': 'english', 'emoji': '✏️', 'type': 'word'},
    # English Sentences
    {'word': 'The cat sat on the mat',          'phoneme': 'k',  'lang': 'english', 'emoji': '🐱', 'type': 'sentence'},
    {'word': 'The bright yellow sun is shining', 'phoneme': 's',  'lang': 'english', 'emoji': '☀️', 'type': 'sentence'},
    {'word': 'A blue butterfly flies high',      'phoneme': 'b',  'lang': 'english', 'emoji': '🦋', 'type': 'sentence'},
    {'word': 'The lion has a big roar',          'phoneme': 'r',  'lang': 'english', 'emoji': '🦁', 'type': 'sentence'},
    {'word': 'I drink sweet cold water',         'phoneme': 'w',  'lang': 'english', 'emoji': '💧', 'type': 'sentence'},
    # Hindi Words
    {'word': 'सूरज',        'phoneme': 'स',   'lang': 'hindi',   'emoji': '☀️', 'type': 'word'},
    {'word': 'माँ',          'phoneme': 'म',   'lang': 'hindi',   'emoji': '👩', 'type': 'word'},
    {'word': 'पानी',         'phoneme': 'प',   'lang': 'hindi',   'emoji': '💧', 'type': 'word'},
    {'word': 'कमल',         'phoneme': 'क',   'lang': 'hindi',   'emoji': '🪷', 'type': 'word'},
    {'word': 'राम',          'phoneme': 'र',   'lang': 'hindi',   'emoji': '🙏', 'type': 'word'},
    {'word': 'आम',           'phoneme': 'अ',   'lang': 'hindi',   'emoji': '🥭', 'type': 'word'},
    {'word': 'मछली',         'phoneme': 'म',   'lang': 'hindi',   'emoji': '🐟', 'type': 'word'},
    {'word': 'गेंद',          'phoneme': 'ग',   'lang': 'hindi',   'emoji': '⚽', 'type': 'word'},
    {'word': 'बिल्ली',        'phoneme': 'ब',   'lang': 'hindi',   'emoji': '🐱', 'type': 'word'},
    {'word': 'फूल',           'phoneme': 'फ',   'lang': 'hindi',   'emoji': '🌸', 'type': 'word'},
    {'word': 'हाथी',          'phoneme': 'ह',   'lang': 'hindi',   'emoji': '🐘', 'type': 'word'},
    {'word': 'तितली',         'phoneme': 'त',   'lang': 'hindi',   'emoji': '🦋', 'type': 'word'},
    {'word': 'नदी',           'phoneme': 'न',   'lang': 'hindi',   'emoji': '🌊', 'type': 'word'},
    {'word': 'पत्ता',          'phoneme': 'प',   'lang': 'hindi',   'emoji': '🍃', 'type': 'word'},
    {'word': 'चाँद',          'phoneme': 'च',   'lang': 'hindi',   'emoji': '🌙', 'type': 'word'},
    {'word': 'गाड़ी',         'phoneme': 'ग',   'lang': 'hindi',   'emoji': '🚗', 'type': 'word'},
    # Hindi Sentences
    {'word': 'सूरज पूर्व से निकलता है',           'phoneme': 'स',  'lang': 'hindi',   'emoji': '☀️', 'type': 'sentence'},
    {'word': 'तितली सुंदर फूलों पर उड़ती है',     'phoneme': 'त',  'lang': 'hindi',   'emoji': '🌸', 'type': 'sentence'},
    {'word': 'पानी बहुत साफ़ और मीठा है',         'phoneme': 'प',  'lang': 'hindi',   'emoji': '💧', 'type': 'sentence'},
    {'word': 'माँ ने मुझे मीठा आम दिया',          'phoneme': 'म',  'lang': 'hindi',   'emoji': '🥭', 'type': 'sentence'},
    {'word': 'सफ़ेद कमल पानी में खिलता है',       'phoneme': 'क',  'lang': 'hindi',   'emoji': '🪷', 'type': 'sentence'},
]


def api_daily_quest(request, child_id):
    """
    Return today's quest items for a child.
    - If child already completed 3+ quest words today, marks quest 100% complete with no more practice needed!
    - Otherwise picks fresh unpracticed items deterministically for today.
    """
    from datetime import datetime, timezone, timedelta
    today = datetime.now(timezone.utc).date()

    # Get child's registered languages
    try:
        child_obj       = ChildProfile.objects.get(id=child_id)
        child_languages = child_obj.get_languages()
    except ChildProfile.DoesNotExist:
        child_languages = ['english']

    lang_pool = [w for w in _QUEST_POOL if w['lang'] in child_languages]
    if not lang_pool:
        lang_pool = [w for w in _QUEST_POOL if w['lang'] == 'english']

    # Check words already completed today
    today_sessions = PracticeSession.objects.filter(
        child_id=child_id,
        created_at__date=today
    ).values_list('recording_id', flat=True)
    completed_today_set = set(
        Recording.objects
        .filter(id__in=today_sessions)
        .exclude(target_word='')
        .values_list('target_word', flat=True)
    )

    # 1. If child already completed 3 or more practices today -> All done for today!
    if len(completed_today_set) >= 3:
        completed_items = []
        for word_str in list(completed_today_set)[:3]:
            # find matching entry in pool or make dynamic entry
            match = next((w for w in lang_pool if w['word'].lower() == word_str.lower()), None)
            if match:
                completed_items.append({**match, 'completed': True})
            else:
                completed_items.append({
                    'word': word_str,
                    'phoneme': word_str[0].lower() if word_str else 's',
                    'lang': child_languages[0] if child_languages else 'english',
                    'emoji': '⭐',
                    'completed': True
                })

        return JsonResponse({
            'success':    True,
            'date':       today.isoformat(),
            'quest':      completed_items,
            'all_done':   True,
            'completed':  len(completed_items),
            'total':      len(completed_items),
        })

    # 2. Child hasn't completed 3 yet -> Pick 3 coherent items
    all_session_ids = PracticeSession.objects.filter(child_id=child_id).values_list('recording_id', flat=True)
    ever_practiced  = set(
        Recording.objects
        .filter(id__in=all_session_ids)
        .exclude(target_word='')
        .values_list('target_word', flat=True)
    )

    # Separate candidates: prioritiy to never practiced, then not today
    never    = [w for w in lang_pool if w['word'] not in ever_practiced and w['word'] not in completed_today_set]
    not_tod  = [w for w in lang_pool if w['word'] not in completed_today_set and w['word'] in ever_practiced]
    fallback = [w for w in lang_pool if w['word'] not in completed_today_set]

    candidate_pool = never + not_tod + fallback
    if not candidate_pool:
        candidate_pool = lang_pool

    import random
    seed = int(today.strftime('%Y%m%d')) + int(child_id)
    rng  = random.Random(seed)
    rng.shuffle(candidate_pool)

    # Pick items to fill up to 3 slots
    quest_items = []

    # Preserve any items already practiced today as completed
    for w in lang_pool:
        if w['word'] in completed_today_set and len(quest_items) < 3:
            quest_items.append({**w, 'completed': True})

    # Fill remaining slots with fresh items
    needed = 3 - len(quest_items)
    for c in candidate_pool:
        if needed <= 0:
            break
        if not any(q['word'] == c['word'] for q in quest_items):
            quest_items.append({**c, 'completed': False})
            needed -= 1

    all_done = len(quest_items) >= 3 and all(q['completed'] for q in quest_items)

    return JsonResponse({
        'success':    True,
        'date':       today.isoformat(),
        'quest':      quest_items,
        'all_done':   all_done,
        'completed':  len([q for q in quest_items if q['completed']]),
        'total':      len(quest_items),
    })


# ── BADGES ───────────────────────────────────────────────
# Badge definitions: (badge_type, emoji, label, check_fn)
def _evaluate_badges(child_id):
    """Evaluate all badge criteria for a child. Returns list of badge dicts with earned=True/False."""
    from datetime import datetime, timezone, timedelta

    # Get child's registered languages
    try:
        child_obj       = ChildProfile.objects.get(id=child_id)
        child_languages = child_obj.get_languages()
    except ChildProfile.DoesNotExist:
        child_languages = ['english']

    has_hindi = 'hindi' in child_languages

    sessions = list(PracticeSession.objects.filter(child_id=child_id).order_by('created_at'))
    total    = len(sessions)

    # Unique words
    all_rec_ids = [s.recording_id for s in sessions if s.recording_id]
    all_words   = set(
        Recording.objects.filter(id__in=all_rec_ids)
        .exclude(target_word='').values_list('target_word', flat=True)
    )

    # Hindi words practiced (only relevant if child has Hindi)
    hindi_words = set(
        Recording.objects.filter(id__in=all_rec_ids, language='hindi')
        .exclude(target_word='').values_list('target_word', flat=True)
    ) if has_hindi else set()

    # ── Streak: count consecutive days ending on today (or yesterday)
    # A streak counts if the child practiced today OR yesterday (graceful for
    # users who haven't practiced yet today).
    today        = datetime.now(timezone.utc).date()
    dates_active = set(s.created_at.date() for s in sessions)
    streak       = 0
    # Start from today; if no session today, start from yesterday
    if today in dates_active:
        check_day = today
    elif (today - timedelta(days=1)) in dates_active:
        check_day = today - timedelta(days=1)
    else:
        check_day = None   # streak is 0

    if check_day:
        while check_day in dates_active:
            streak   += 1
            check_day -= timedelta(days=1)

    # Total stars
    total_stars = sum(
        (3 if s.score >= 88 else 2 if s.score >= 70 else 1 if s.score >= 50 else 0)
        for s in sessions
    )

    # Perfect scores (>=95)
    perfect = sum(1 for s in sessions if s.score >= 95)

    # Badge definitions — Hindi Word badge only shown if child has Hindi in their languages
    all_badges = [
        {
            'badge_type': 'first_practice',
            'emoji':      '🌱',
            'label':      'First Practice',
            'desc':       'Complete your very first practice session',
            'earned':     total >= 1,
        },
        {
            'badge_type': 'streak_3',
            'emoji':      '🔥',
            'label':      '3-Day Streak',
            'desc':       'Practice 3 days in a row',
            'earned':     streak >= 3,
        },
        {
            'badge_type': 'stars_10',
            'emoji':      '⭐',
            'label':      '10 Stars',
            'desc':       'Earn 10 stars total',
            'earned':     total_stars >= 10,
        },
        {
            'badge_type': 'perfect_score',
            'emoji':      '🏅',
            'label':      'Perfect Score',
            'desc':       'Score 95% or above',
            'earned':     perfect >= 1,
        },
        {
            'badge_type': 'words_10',
            'emoji':      '📚',
            'label':      'Word Explorer',
            'desc':       'Practice 10 different words',
            'earned':     len(all_words) >= 10,
        },
        {
            'badge_type': 'streak_7',
            'emoji':      '🌟',
            'label':      '7-Day Streak',
            'desc':       'Practice 7 days in a row',
            'earned':     streak >= 7,
        },
        {
            'badge_type': 'sessions_25',
            'emoji':      '🏆',
            'label':      'Super Speaker',
            'desc':       'Complete 25 practice sessions',
            'earned':     total >= 25,
        },
    ]

    # Hindi Word badge — only add if child has Hindi in their languages
    if has_hindi:
        all_badges.insert(3, {
            'badge_type': 'hindi_word',
            'emoji':      '🎵',
            'label':      'Hindi Word',
            'desc':       'Practice a Hindi word',
            'earned':     len(hindi_words) >= 1,
        })

    # Persist newly earned badges using Django ORM
    existing = set(Badge.objects.filter(child_id=child_id).values_list('badge_type', flat=True))
    for b in all_badges:
        if b['earned'] and b['badge_type'] not in existing:
            Badge.objects.create(
                child_id=child_id,
                badge_type=b['badge_type'],
                badge_name=b['label'],
            )

    return all_badges


def api_badges(request, child_id):
    """Return all badge definitions with earned/locked state for this child."""
    badges = _evaluate_badges(child_id)
    return JsonResponse({'success': True, 'badges': badges})
