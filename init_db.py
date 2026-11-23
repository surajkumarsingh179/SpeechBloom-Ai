"""
SpeechBloom AI - Database Initialization Script

Run this once to create all tables and seed sample exercises:
    python init_db.py

This script:
1. Creates all SQLite database tables
2. Seeds Hindi and English speech exercises
3. Creates required directories (uploads, model storage)
"""
import sys
import os

# Ensure the project root is on the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import db
from backend.models.exercise import Exercise


def seed_exercises():
    """Populate the database with starter exercises for Hindi and English."""

    exercises = [
        # ── English: Articulation ──────────────────────────────────────
        Exercise(language='english', category='articulation', target_word='Red',
                 target_phoneme='r', difficulty=1,
                 instructions='Say the word "Red" clearly. Focus on the "r" sound at the beginning.',
                 image_hint='🔴'),
        Exercise(language='english', category='articulation', target_word='Sun',
                 target_phoneme='s', difficulty=1,
                 instructions='Say the word "Sun" clearly. Focus on the "s" sound.',
                 image_hint='☀️'),
        Exercise(language='english', category='articulation', target_word='Ball',
                 target_phoneme='b', difficulty=1,
                 instructions='Say the word "Ball" clearly. Focus on the "b" sound.',
                 image_hint='⚽'),
        Exercise(language='english', category='articulation', target_word='Cat',
                 target_phoneme='k', difficulty=1,
                 instructions='Say the word "Cat" clearly. Focus on the hard "c" sound.',
                 image_hint='🐱'),
        Exercise(language='english', category='articulation', target_word='Dog',
                 target_phoneme='d', difficulty=1,
                 instructions='Say the word "Dog" clearly. Focus on the "d" sound.',
                 image_hint='🐕'),
        Exercise(language='english', category='articulation', target_word='Fish',
                 target_phoneme='f', difficulty=2,
                 instructions='Say the word "Fish" clearly. Focus on the "f" sound.',
                 image_hint='🐟'),
        Exercise(language='english', category='articulation', target_word='Green',
                 target_phoneme='gr', difficulty=2,
                 instructions='Say the word "Green" clearly. Focus on the "gr" blend.',
                 image_hint='💚'),
        Exercise(language='english', category='articulation', target_word='Ship',
                 target_phoneme='sh', difficulty=2,
                 instructions='Say the word "Ship" clearly. Focus on the "sh" sound.',
                 image_hint='🚢'),
        Exercise(language='english', category='articulation', target_word='Thumb',
                 target_phoneme='th', difficulty=3,
                 instructions='Say the word "Thumb" clearly. Focus on the "th" sound.',
                 image_hint='👍'),
        Exercise(language='english', category='articulation', target_word='Butterfly',
                 target_phoneme='b', difficulty=3,
                 instructions='Say the word "Butterfly" clearly. It has three syllables: but-ter-fly.',
                 image_hint='🦋'),
        Exercise(language='english', category='articulation', target_word='Rabbit',
                 target_phoneme='r', difficulty=2,
                 instructions='Say the word "Rabbit" clearly. Focus on the "r" at the start.',
                 image_hint='🐰'),
        Exercise(language='english', category='articulation', target_word='Lion',
                 target_phoneme='l', difficulty=2,
                 instructions='Say the word "Lion" clearly. Focus on the "l" sound.',
                 image_hint='🦁'),

        # ── English: Phoneme ───────────────────────────────────────────
        Exercise(language='english', category='phoneme', target_word='Apple',
                 target_phoneme='æ', difficulty=1,
                 instructions='Say "Apple". Notice the short "a" sound at the start.',
                 image_hint='🍎'),
        Exercise(language='english', category='phoneme', target_word='Elephant',
                 target_phoneme='ɛ', difficulty=2,
                 instructions='Say "Elephant". Focus on the "eh" sound at the beginning.',
                 image_hint='🐘'),
        Exercise(language='english', category='phoneme', target_word='Ice cream',
                 target_phoneme='aɪ', difficulty=2,
                 instructions='Say "Ice cream". Notice the long "i" sound.',
                 image_hint='🍦'),
        Exercise(language='english', category='phoneme', target_word='Orange',
                 target_phoneme='ɔ', difficulty=2,
                 instructions='Say "Orange". Focus on the "or" sound.',
                 image_hint='🍊'),
        Exercise(language='english', category='phoneme', target_word='Umbrella',
                 target_phoneme='ʌ', difficulty=3,
                 instructions='Say "Umbrella". Focus on the "uh" sound at the start.',
                 image_hint='☂️'),

        # ── English: Word ──────────────────────────────────────────────
        Exercise(language='english', category='word', target_word='Hello',
                 target_phoneme='h', difficulty=1,
                 instructions='Say "Hello" with a clear "h" at the beginning.',
                 image_hint='👋'),
        Exercise(language='english', category='word', target_word='Thank you',
                 target_phoneme='θ', difficulty=2,
                 instructions='Say "Thank you". Practice the "th" sound carefully.',
                 image_hint='🙏'),
        Exercise(language='english', category='word', target_word='Beautiful',
                 target_phoneme='b', difficulty=3,
                 instructions='Say "Beautiful" slowly. It has three syllables: beau-ti-ful.',
                 image_hint='🌸'),
        Exercise(language='english', category='word', target_word='Banana',
                 target_phoneme='b', difficulty=1,
                 instructions='Say "Banana". It has three syllables: ba-na-na.',
                 image_hint='🍌'),

        # ── English: Sentence ──────────────────────────────────────────
        Exercise(language='english', category='sentence', target_word='The cat sat on the mat',
                 target_phoneme='æ', difficulty=2,
                 instructions='Say the whole sentence: "The cat sat on the mat."',
                 image_hint='🐱'),
        Exercise(language='english', category='sentence', target_word='She sells seashells',
                 target_phoneme='sh', difficulty=4,
                 instructions='Say: "She sells seashells." This is a fun tongue twister!',
                 image_hint='🐚'),
        Exercise(language='english', category='sentence', target_word='I love my family',
                 target_phoneme='l', difficulty=1,
                 instructions='Say: "I love my family." Nice and clear!',
                 image_hint='👨‍👩‍👧‍👦'),

        # ── Hindi: Articulation ────────────────────────────────────────
        Exercise(language='hindi', category='articulation', target_word='राम',
                 target_phoneme='र', difficulty=1,
                 instructions='कहिए "राम"। "र" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='🙏'),
        Exercise(language='hindi', category='articulation', target_word='माँ',
                 target_phoneme='म', difficulty=1,
                 instructions='कहिए "माँ"। "म" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='👩'),
        Exercise(language='hindi', category='articulation', target_word='पानी',
                 target_phoneme='प', difficulty=1,
                 instructions='कहिए "पानी"। "प" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='💧'),
        Exercise(language='hindi', category='articulation', target_word='कमल',
                 target_phoneme='क', difficulty=1,
                 instructions='कहिए "कमल"। "क" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='🪷'),
        Exercise(language='hindi', category='articulation', target_word='सूरज',
                 target_phoneme='स', difficulty=1,
                 instructions='कहिए "सूरज"। "स" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='☀️'),
        Exercise(language='hindi', category='articulation', target_word='गेंद',
                 target_phoneme='ग', difficulty=1,
                 instructions='कहिए "गेंद"। "ग" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='⚽'),
        Exercise(language='hindi', category='articulation', target_word='चिड़िया',
                 target_phoneme='च', difficulty=2,
                 instructions='कहिए "चिड़िया"। "च" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='🐦'),
        Exercise(language='hindi', category='articulation', target_word='तितली',
                 target_phoneme='त', difficulty=2,
                 instructions='कहिए "तितली"। "त" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='🦋'),
        Exercise(language='hindi', category='articulation', target_word='खरगोश',
                 target_phoneme='ख', difficulty=2,
                 instructions='कहिए "खरगोश"। "ख" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='🐰'),
        Exercise(language='hindi', category='articulation', target_word='झरना',
                 target_phoneme='झ', difficulty=3,
                 instructions='कहिए "झरना"। "झ" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='🌊'),
        Exercise(language='hindi', category='articulation', target_word='फूल',
                 target_phoneme='फ', difficulty=1,
                 instructions='कहिए "फूल"। "फ" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='🌺'),
        Exercise(language='hindi', category='articulation', target_word='नदी',
                 target_phoneme='न', difficulty=1,
                 instructions='कहिए "नदी"। "न" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='🏞️'),

        # ── Hindi: Phoneme ─────────────────────────────────────────────
        Exercise(language='hindi', category='phoneme', target_word='आम',
                 target_phoneme='आ', difficulty=1,
                 instructions='कहिए "आम"। "आ" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='🥭'),
        Exercise(language='hindi', category='phoneme', target_word='ऊँट',
                 target_phoneme='ऊ', difficulty=2,
                 instructions='कहिए "ऊँट"। "ऊ" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='🐪'),
        Exercise(language='hindi', category='phoneme', target_word='ऐनक',
                 target_phoneme='ऐ', difficulty=2,
                 instructions='कहिए "ऐनक"। "ऐ" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='👓'),
        Exercise(language='hindi', category='phoneme', target_word='औरत',
                 target_phoneme='औ', difficulty=2,
                 instructions='कहिए "औरत"। "औ" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='👩'),
        Exercise(language='hindi', category='phoneme', target_word='इमली',
                 target_phoneme='इ', difficulty=1,
                 instructions='कहिए "इमली"। "इ" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='🌿'),

        # ── Hindi: Word ────────────────────────────────────────────────
        Exercise(language='hindi', category='word', target_word='नमस्ते',
                 target_phoneme='न', difficulty=1,
                 instructions='कहिए "नमस्ते"। यह अभिवादन का शब्द है।',
                 image_hint='🙏'),
        Exercise(language='hindi', category='word', target_word='धन्यवाद',
                 target_phoneme='ध', difficulty=2,
                 instructions='कहिए "धन्यवाद"। "ध" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='😊'),
        Exercise(language='hindi', category='word', target_word='विद्यालय',
                 target_phoneme='व', difficulty=3,
                 instructions='कहिए "विद्यालय"। इसमें चार अक्षर हैं: वि-द्या-ल-य।',
                 image_hint='🏫'),
        Exercise(language='hindi', category='word', target_word='परिवार',
                 target_phoneme='प', difficulty=2,
                 instructions='कहिए "परिवार"। "प" और "र" की ध्वनि पर ध्यान दीजिए।',
                 image_hint='👨‍👩‍👧‍👦'),

        # ── Hindi: Sentence ────────────────────────────────────────────
        Exercise(language='hindi', category='sentence', target_word='मेरा नाम',
                 target_phoneme='म', difficulty=1,
                 instructions='कहिए "मेरा नाम ___"। अपना नाम बोलिए।',
                 image_hint='👤'),
        Exercise(language='hindi', category='sentence', target_word='आज मौसम अच्छा है',
                 target_phoneme='म', difficulty=3,
                 instructions='पूरा वाक्य कहिए: "आज मौसम अच्छा है।"',
                 image_hint='🌤️'),
        Exercise(language='hindi', category='sentence', target_word='मुझे खेलना पसंद है',
                 target_phoneme='म', difficulty=2,
                 instructions='पूरा वाक्य कहिए: "मुझे खेलना पसंद है।"',
                 image_hint='🎮'),
    ]

    existing_count = Exercise.query.count()
    if existing_count > 0:
        print(f"  Database already has {existing_count} exercises. Skipping seed.")
        return existing_count

    for ex in exercises:
        db.session.add(ex)
    db.session.commit()

    hindi_count = sum(1 for e in exercises if e.language == 'hindi')
    english_count = sum(1 for e in exercises if e.language == 'english')
    print(f"  Seeded {len(exercises)} exercises ({english_count} English, {hindi_count} Hindi)")
    return len(exercises)


def init():
    """Initialize database, seed data, and create directories."""
    # Import here to avoid circular imports at module level
    from app import create_app

    app = create_app()

    with app.app_context():
        print("=" * 50)
        print("  SpeechBloom AI - Database Initialization")
        print("=" * 50)

        # Create tables
        print("\n1. Creating database tables...")
        db.create_all()
        print("   ✅ Tables created successfully!")

        # Seed exercises
        print("\n2. Seeding exercises...")
        seed_exercises()

        # Create directories
        print("\n3. Creating directories...")
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        print(f"   ✅ Upload directory: {app.config['UPLOAD_FOLDER']}")
        os.makedirs(app.config['MODEL_PATH'], exist_ok=True)
        print(f"   ✅ Model directory: {app.config['MODEL_PATH']}")

        # Summary
        print("\n" + "=" * 50)
        print("  ✅ Initialization complete!")
        print(f"  Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"  Demo mode: {app.config['DEMO_MODE']}")
        print("=" * 50)
        print("\nNext steps:")
        print("  python app.py")
        print("  Then open http://localhost:5000 in your browser")


if __name__ == '__main__':
    init()
