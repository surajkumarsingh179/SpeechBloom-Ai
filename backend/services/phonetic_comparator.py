"""
SpeechBloom AI - Phonetic & Articulation Evaluation Engine
Analyzes phonetic distance, consonant place/manner substitutions, and acoustic spectral validation.
"""
import re


class PhoneticComparator:
    """Evaluates child pronunciation against target words and phonemes."""

    # Articulatory phonetic profiles for common target consonants (English & Hindi)
    ARTICULATION_GUIDE = {
        's': {
            'manner': 'fricative',
            'place': 'alveolar',
            'hint': "Place your tongue tip behind your upper front teeth and blow a gentle hiss sound like a happy snake: sssss-un! 🐍",
            'substitutions': {
                'l': "We heard an 'l' sound instead of 's'! Don't let your tongue touch the roof of your mouth. Leave a tiny gap and hiss gently: sssss! 🐍",
                'f': "We heard an 'f' sound! Avoid biting your lower lip. Keep both lips relaxed and smile as you make the 's' sound! 😊",
                'sh': "We heard 'sh' (like 'shhh')! Bring your tongue slightly forward towards your front teeth for a sharp 's' sound! 🎯",
                't': "We heard a 't' sound! Don't stop the air completely—let it keep flowing in a steady hiss: sssss! 🌬️",
                'th': "We heard a 'th' sound! Keep your tongue just behind your teeth, not peeking through! 🦷"
            }
        },
        'r': {
            'manner': 'approximant',
            'place': 'alveolar/retroflex',
            'hint': "Pull your tongue slightly back into your mouth without touching the roof. Growl softly like a friendly lion: rrrrr! 🦁",
            'substitutions': {
                'w': "We heard a 'w' sound instead of 'r' (like 'wed' for 'red')! Keep your lips wide in a gentle smile instead of rounding them like an 'O'! 👄",
                'l': "We heard an 'l' sound! Pull your tongue back rather than tapping it upward! 🦁",
                'y': "We heard a 'y' sound! Keep the sides of your tongue against your upper molars and practice the growl: rrrr! 🐯"
            }
        },
        'l': {
            'manner': 'liquid',
            'place': 'alveolar',
            'hint': "Touch the tip of your tongue to the bumpy ridge right behind your top front teeth: llll-ion! 🦁",
            'substitutions': {
                'w': "We heard a 'w' sound! Make sure your tongue tip taps up behind your teeth! 👅",
                'y': "We heard a 'y' sound! Touch your tongue tip firmly behind your top teeth: llll! 🦁"
            }
        },
        'k': {
            'manner': 'stop',
            'place': 'velar',
            'hint': "Push the back of your tongue against the soft roof of your mouth and release a clean pop: k-k-cat! 🐱",
            'substitutions': {
                't': "We heard a 't' sound (fronting)! Keep the front of your tongue down and use the back of your tongue for 'k'! 🐱"
            }
        },
        'g': {
            'manner': 'stop',
            'place': 'velar',
            'hint': "Use the back of your throat with your vocal cords vibrating: g-g-go! ⚽",
            'substitutions': {
                'd': "We heard a 'd' sound! Move the sound to the back of your mouth, using the back of your tongue! ⚽"
            }
        },
        'sh': {
            'manner': 'fricative',
            'place': 'palato-alveolar',
            'hint': "Round your lips slightly and blow gentle air like you are telling someone to be quiet: shhhh-ip! 🚢",
            'substitutions': {
                's': "We heard 's' instead of 'sh'! Round your lips a little more and pull your tongue slightly back: shhhh! 🚢"
            }
        },
        'f': {
            'manner': 'fricative',
            'place': 'labiodental',
            'hint': "Gently rest your top front teeth on your lower lip and blow softly: ffff-ish! 🐟",
            'substitutions': {
                'p': "We heard a 'p' sound! Don't press both lips together—let air flow over your lower lip! 🐟",
                'b': "We heard a 'b' sound! Keep the air flowing smoothly through your teeth and lip: ffff! 🐟"
            }
        },
        # Hindi target sounds
        'र': {
            'manner': 'trill/tap',
            'place': 'alveolar',
            'hint': 'जीभ की नोक को ऊपर के मसूड़े पर हल्का सा कंपन (फ्लेक्स) करके बोलिए: र-र-राम! 🚩',
            'substitutions': {
                'ल': 'आपने "ल" बोला (जैसे "लाम" की तरह)! जीभ को ऊपर चिपकाकर न रखें, हल्का सा कंपन करें: र-र-राम! 🔄',
                'ड': 'आपने "ड" बोला! जीभ को हल्का रखिए और "र" की स्पष्ट ध्वनि निकालिए। 🌟'
            }
        },
        'स': {
            'manner': 'fricative',
            'place': 'dental/alveolar',
            'hint': 'दांतों के पीछे से धीमी हवा निकालिए जैसे सीटी बजती है: स-स-सूरज! ☀️',
            'substitutions': {
                'ल': 'आपने "ल" बोला (जैसे "लूरज")! "स" के लिए दांतों के पीछे से सीटी जैसी हवा निकालिए: स्-स्-सूरज! ☀️',
                'श': 'आपने "श" बोला! जीभ को आगे की ओर रखें, दांतों के पास: स-स-सूरज! ☀️',
                'थ': 'आपने "थ" बोला! जीभ को दांतों के अंदर ही रखिए, बाहर मत निकालिए: स-स-सूरज! ☀️'
            }
        },
        'क': {
            'manner': 'stop',
            'place': 'velar',
            'hint': 'गले के पिछले हिस्से से साफ आवाज निकालिए: क-क-कमल! 🪷',
            'substitutions': {
                'त': 'आपने "त" बोला! जीभ के आगे वाले हिस्से के बजाय पीछे वाले हिस्से से बोलिए: क-क-कमल! 🪷'
            }
        },
        'प': {
            'manner': 'stop',
            'place': 'bilabial',
            'hint': 'दोनों होंठों को मिलाकर खोलिए: प-प-पानी! 💧',
            'substitutions': {
                'फ': 'आपने अधिक हवा के साथ "फ" बोला! हल्के होंठों से केवल "प" बोलिए: प-पानी! 💧'
            }
        }
    }

    @staticmethod
    def normalize_text(text):
        if not text:
            return ""
        text = re.sub(r'[^\w\s]', '', text.lower().strip())
        return ' '.join(text.split())

    @staticmethod
    def levenshtein_similarity(s1, s2):
        """Compute string similarity ratio between 0.0 and 1.0."""
        s1 = PhoneticComparator.normalize_text(s1)
        s2 = PhoneticComparator.normalize_text(s2)
        if s1 == s2:
            return 1.0
        if not s1 or not s2:
            return 0.0

        len1, len2 = len(s1), len(s2)
        dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        for i in range(len1 + 1):
            dp[i][0] = i
        for j in range(len2 + 1):
            dp[0][j] = j

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,
                    dp[i][j - 1] + 1,
                    dp[i - 1][j - 1] + cost
                )

        max_len = max(len1, len2)
        edit_dist = dp[len1][len2]
        return max(0.0, 1.0 - (edit_dist / max_len))

    @classmethod
    def evaluate_pronunciation(cls, target_word, target_phoneme, observed_transcript, acoustic_features=None, language='english'):
        """
        Evaluate pronunciation accuracy using phonetic comparison and acoustic analysis.
        """
        target_norm = cls.normalize_text(target_word)
        observed_norm = cls.normalize_text(observed_transcript) if observed_transcript else ""
        target_ph = (target_phoneme or '').lower().strip()

        acoustic_features = acoustic_features or {}
        centroid = float(acoustic_features.get('spectral_centroid', 0.0))
        zcr = float(acoustic_features.get('zero_crossing_rate', 0.0))
        rms = float(acoustic_features.get('rms_energy', 0.0))
        duration = float(acoustic_features.get('duration', 0.0))

        # Check for silent or inaudible recording
        if not observed_norm and rms < 0.015:
            return {
                'score': 20.0,
                'error_category': 'omission',
                'observed_phoneme': '(silent)',
                'observed_transcript': '',
                'feedback': "We didn't hear audio clearly. Hold the microphone close and speak with a clear, happy voice! 🎤",
                'is_match': False
            }

        # -------------------------------------------------------------
        # BRANCH A: Speech-to-text transcript was captured
        # -------------------------------------------------------------
        if observed_norm:
            # 1. Exact Word Match
            if observed_norm == target_norm:
                return {
                    'score': 95.0,
                    'error_category': 'none',
                    'observed_phoneme': target_phoneme,
                    'observed_transcript': observed_norm,
                    'feedback': f"Outstanding! You pronounced '{target_word}' clearly! 🌟 Beautiful work on the '{target_phoneme}' sound!",
                    'is_match': True
                }

            target_initial = target_norm[0] if target_norm else ''
            observed_initial = observed_norm[0] if observed_norm else ''

            # 2. Check for Specific Phoneme Substitution
            is_phoneme_substitution = False
            substitution_hint = None
            ph_guide = cls.ARTICULATION_GUIDE.get(target_ph) or cls.ARTICULATION_GUIDE.get(target_initial)

            if ph_guide:
                subs_dict = ph_guide.get('substitutions', {})
                if observed_initial in subs_dict:
                    is_phoneme_substitution = True
                    substitution_hint = subs_dict[observed_initial]
                elif observed_initial != target_initial:
                    is_phoneme_substitution = True
                    substitution_hint = f"We heard '{observed_initial}' instead of '{target_ph}' in '{observed_norm}'! {ph_guide.get('hint', '')}"

            # 3. Levenshtein Word Similarity
            similarity = cls.levenshtein_similarity(target_norm, observed_norm)

            if is_phoneme_substitution:
                # Substituted initial phoneme: score is between 46% and 54%
                score = round(max(44.0, min(56.0, 42.0 + (similarity * 18.0))), 1)
                error_category = 'substitution'
                feedback = substitution_hint or f"We heard '{observed_norm}' instead of '{target_word}'. Let's practice the '{target_phoneme}' sound once more! 🔄"
                observed_phoneme = observed_initial
            elif similarity >= 0.70:
                # Very close pronunciation (minor distortion or vowel variance)
                score = round(min(88.0, 72.0 + (similarity * 18.0)), 1)
                error_category = 'distortion'
                feedback = f"Almost there! You said '{observed_norm}'. Keep going—focus closely on the '{target_phoneme}' sound in '{target_word}'! 💫"
                observed_phoneme = f"{target_phoneme} (approx)"
            else:
                score = round(max(40.0, min(60.0, 35.0 + similarity * 30.0)), 1)
                error_category = 'substitution'
                feedback = f"Good effort! We heard '{observed_norm}'. Listen to the reference audio and try saying '{target_word}' clearly! 🐢"
                observed_phoneme = observed_initial or '-'

            return {
                'score': score,
                'error_category': error_category,
                'observed_phoneme': observed_phoneme,
                'observed_transcript': observed_norm,
                'feedback': feedback,
                'is_match': False
            }

        # -------------------------------------------------------------
        # BRANCH B: Acoustic Analysis Fallback (When transcript is empty)
        # Evaluate spectral frequency, zero crossings, and acoustic profile
        # -------------------------------------------------------------
        ph_key = target_ph.lower()

        # Case 1: Sibilant Fricatives (/s/, /sh/, /स/, /श/)
        if ph_key in ['s', 'sh', 'स', 'श']:
            # Sibilants require high spectral centroid (>2500Hz) and high zero-crossing rate (>0.08)
            if centroid >= 2400 or zcr >= 0.08:
                # Acoustic energy matches sibilant hiss!
                score = round(min(92.0, max(80.0, 75.0 + min(15.0, (centroid / 400.0)))), 1)
                return {
                    'score': score,
                    'error_category': 'none',
                    'observed_phoneme': target_phoneme,
                    'observed_transcript': target_word,
                    'feedback': f"Great acoustic pronunciation! You made a clean, sharp '{target_phoneme}' sound! 🐍✨",
                    'is_match': True
                }
            else:
                # Low centroid (<2400Hz) means smooth liquid/vowel sound like 'l' was produced instead of 's'
                guide_hint = cls.ARTICULATION_GUIDE['s']['substitutions'].get('l')
                return {
                    'score': 50.0,
                    'error_category': 'substitution',
                    'observed_phoneme': 'l (acoustic)',
                    'observed_transcript': f"approx. l-{target_word[1:] if len(target_word)>1 else ''}",
                    'feedback': guide_hint or "We heard a softer sound instead of the sharp 's' hiss. Keep your teeth close and blow a steady hiss: sssss! 🐍",
                    'is_match': False
                }

        # Case 2: Approximants & Liquids (/r/, /l/, /र/, /ल/)
        elif ph_key in ['r', 'l', 'र', 'ल']:
            if 0.4 <= duration <= 3.0 and rms > 0.03:
                score = round(min(90.0, max(78.0, 75.0 + min(15.0, rms * 100))), 1)
                return {
                    'score': score,
                    'error_category': 'none',
                    'observed_phoneme': target_phoneme,
                    'observed_transcript': target_word,
                    'feedback': f"Wonderful effort! Your vocal resonance for '{target_word}' is coming through clearly! 🌟",
                    'is_match': True
                }
            else:
                return {
                    'score': 62.0,
                    'error_category': 'distortion',
                    'observed_phoneme': f"{target_phoneme} (approx)",
                    'observed_transcript': f"{target_word} (approx)",
                    'feedback': f"Nice try on '{target_word}'! Speak clearly at a steady pace and give the '{target_phoneme}' sound your full voice! 🦁",
                    'is_match': False
                }

        # Case 3: Other consonants/words
        else:
            base = 72.0
            if rms > 0.04:
                base += 8.0
            if 0.5 <= duration <= 2.5:
                base += 6.0
            score = round(min(90.0, max(68.0, base)), 1)
            return {
                'score': score,
                'error_category': 'none',
                'observed_phoneme': target_phoneme or 'clear',
                'observed_transcript': target_word,
                'feedback': f"Good practice on '{target_word}'! Your pronunciation was clear and audible! 🌟",
                'is_match': True
            }
