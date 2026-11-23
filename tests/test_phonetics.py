"""
SpeechBloom AI - Phonetic Evaluation Unit Tests
"""
import unittest
from backend.services.phonetic_comparator import PhoneticComparator
from backend.services.ml_service import MLService


class PhoneticEvaluationTestCase(unittest.TestCase):
    def setUp(self):
        self.ml = MLService()

    def test_sun_vs_lun_substitution(self):
        """When child says 'lun' instead of 'Sun', score must be ~51% (substitution)."""
        res = self.ml.analyze(
            features_dict={'rms_energy': 0.1, 'duration': 1.0, 'spectral_centroid': 1400.0},
            target_word='Sun',
            target_phoneme='s',
            observed_transcript='lun',
            language='english'
        )
        print("\n[TEST: Sun vs lun]")
        print("Score:", res['score'])
        print("Category:", res['error_category'])
        print("Feedback:", res['feedback'])

        self.assertLessEqual(res['score'], 60.0)
        self.assertGreaterEqual(res['score'], 45.0)
        self.assertEqual(res['error_category'], 'substitution')
        self.assertIn("'l'", res['feedback'])

    def test_sun_exact_match(self):
        """When child says 'Sun' correctly, score must be high (>= 90%)."""
        res = self.ml.analyze(
            features_dict={'rms_energy': 0.1, 'duration': 1.0, 'spectral_centroid': 4500.0},
            target_word='Sun',
            target_phoneme='s',
            observed_transcript='sun',
            language='english'
        )
        print("\n[TEST: Sun exact match]")
        print("Score:", res['score'])
        self.assertGreaterEqual(res['score'], 90.0)
        self.assertEqual(res['error_category'], 'none')

    def test_acoustic_sibilant_match_without_transcript(self):
        """When speech-to-text is silent but acoustic profile has high sibilant frequency."""
        res = self.ml.analyze(
            features_dict={'rms_energy': 0.08, 'duration': 1.2, 'spectral_centroid': 3400.0, 'zero_crossing_rate': 0.14},
            target_word='Sun',
            target_phoneme='s',
            observed_transcript='',
            language='english'
        )
        print("\n[TEST: Acoustic sibilant match]")
        print("Score:", res['score'])
        print("Category:", res['error_category'])
        self.assertGreaterEqual(res['score'], 80.0)
        self.assertEqual(res['error_category'], 'none')

    def test_acoustic_sibilant_mismatch_without_transcript(self):
        """When speech-to-text is silent but acoustic profile lacks high frequency hiss."""
        res = self.ml.analyze(
            features_dict={'rms_energy': 0.08, 'duration': 1.2, 'spectral_centroid': 1400.0, 'zero_crossing_rate': 0.04},
            target_word='Sun',
            target_phoneme='s',
            observed_transcript='',
            language='english'
        )
        print("\n[TEST: Acoustic sibilant mismatch]")
        print("Score:", res['score'])
        print("Category:", res['error_category'])
        self.assertEqual(res['score'], 50.0)
        self.assertEqual(res['error_category'], 'substitution')

    def test_red_vs_wed_gliding(self):
        """When child says 'wed' instead of 'red'."""
        res = self.ml.analyze(
            features_dict={'rms_energy': 0.1, 'duration': 1.0},
            target_word='Red',
            target_phoneme='r',
            observed_transcript='wed',
            language='english'
        )
        print("\n[TEST: Red vs wed]")
        print("Score:", res['score'])
        self.assertLessEqual(res['score'], 60.0)
        self.assertEqual(res['error_category'], 'substitution')

    def test_hindi_ram_vs_laam(self):
        """When child says 'लाम' instead of 'राम' in Hindi."""
        res = self.ml.analyze(
            features_dict={'rms_energy': 0.1, 'duration': 1.0},
            target_word='राम',
            target_phoneme='र',
            observed_transcript='लाम',
            language='hindi'
        )
        print("\n[TEST: राम vs लाम]")
        print("Score:", res['score'])
        self.assertLessEqual(res['score'], 60.0)
        self.assertEqual(res['error_category'], 'substitution')


if __name__ == '__main__':
    unittest.main()
