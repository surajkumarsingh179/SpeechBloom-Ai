"""
SpeechBloom AI - Django Automated System Tests
Tests Parent signup -> Add child -> Daily speech practice -> Detailed reports -> Supabase sync
"""
import json
from django.test import TestCase, Client
from core.models import ParentUser, ChildProfile, Exercise, PracticeSession


class SpeechBloomDjangoTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_parent_signup_and_child_flow(self):
        # 1. Parent registers
        signup_data = {
            'name': 'Pooja Verma',
            'email': 'pooja@example.com',
            'password': 'password123',
            'role': 'parent'
        }
        res = self.client.post('/api/register', data=json.dumps(signup_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res_data = res.json()
        self.assertTrue(res_data['success'])
        self.assertEqual(res_data['redirect_url'], '/profile/')

        # 2. Parent logs in
        login_data = {'email': 'pooja@example.com', 'password': 'password123'}
        res = self.client.post('/api/login', data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(res.status_code, 200)

        # 3. Parent adds child profile
        child_data = {
            'name': 'Rohan',
            'age': 5,
            'avatar': '🦁',
            'languages': ['hindi', 'english']
        }
        res = self.client.post('/api/children', data=json.dumps(child_data), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        child_id = res.json()['child']['id']

        # 4. Parent views parent dashboard with reports
        res = self.client.get('/api/dashboard/parent')
        self.assertEqual(res.status_code, 200)
        dash_data = res.json()
        self.assertTrue(dash_data['success'])
        self.assertEqual(dash_data['total_children'], 1)
        self.assertEqual(dash_data['children_summary'][0]['child']['name'], 'Rohan')

    def test_pages_render(self):
        # Set session parent
        p = ParentUser.objects.create(email='sessionparent@speechbloom.ai', name='Session Parent')
        session = self.client.session
        session['user_id'] = str(p.id)
        session['parent_id'] = str(p.id)
        session['parent_email'] = p.email
        session.save()

        routes = ['/', '/login/', '/register/', '/profile/', '/parent/', '/practice/', '/recording/', '/games/', '/progress/']
        for r in routes:
            res = self.client.get(r)
            self.assertEqual(res.status_code, 200, f"Route {r} failed with {res.status_code}")

    def test_ai_engine_phonetic_scoring(self):
        # Verify phonetic scoring: 'sun' vs 'lun'
        parent = ParentUser.objects.create(email='testparent@speechbloom.ai', name='Test Parent')
        child = ChildProfile.objects.create(parent=parent, name='Kid', age=5)

        # Upload dummy WAV audio
        from django.core.files.uploadedfile import SimpleUploadedFile
        wav_content = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80>\x00\x00\x00}\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00'
        audio_file = SimpleUploadedFile("speech.wav", wav_content, content_type="audio/wav")

        rec_res = self.client.post('/api/recording', {
            'audio': audio_file,
            'child_id': child.id,
            'target_word': 'Sun',
            'target_phoneme': 's',
            'observed_transcript': 'lun'
        })
        self.assertEqual(rec_res.status_code, 201)
        rec_id = rec_res.json()['recording_id']

        # Analyze
        analyze_res = self.client.post('/api/analyze', data=json.dumps({
            'recording_id': rec_id,
            'observed_transcript': 'lun'
        }), content_type='application/json')
        self.assertEqual(analyze_res.status_code, 200)
        data = analyze_res.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['error_category'], 'substitution')
        self.assertLessEqual(data['score'], 60.0)
