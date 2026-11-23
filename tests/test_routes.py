"""
SpeechBloom AI - Automated Route & Endpoint Tests
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from database import db


class SpeechBloomTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_pages(self):
        routes = [
            '/',
            '/login',
            '/register',
            '/practice',
            '/recording',
            '/games',
            '/games/repeat',
            '/games/explorer',
            '/games/matching',
            '/games/picture',
            '/games/phoneme',
            '/games/quest',
            '/progress',
            '/about',
            '/dataset-info',
            '/dashboard',
            '/profile'
        ]
        for route in routes:
            with self.subTest(route=route):
                res = self.client.get(route)
                self.assertEqual(res.status_code, 200, f"Route {route} failed with {res.status_code}")

    def test_api_exercises(self):
        res = self.client.get('/api/exercises?language=hindi')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertGreater(data['count'], 0)

    def test_api_model_status(self):
        res = self.client.get('/api/model/status')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('status', data)

    def test_api_progress(self):
        res = self.client.get('/api/progress/1')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('stats', data)


if __name__ == '__main__':
    unittest.main()
