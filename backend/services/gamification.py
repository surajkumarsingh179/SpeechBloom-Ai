"""
SpeechBloom AI - Gamification Service (Django-compatible)
Handles star rewards, encouragement messages, and level progression.
Badge logic uses Django ORM (core.models).
"""
import random


class GamificationService:
    """Calculates stars, encouragement, levels, and quests."""

    @staticmethod
    def calculate_stars(score):
        """Map score 0-100 to 0–3 stars."""
        if score >= 88:
            return 3
        elif score >= 70:
            return 2
        elif score >= 50:
            return 1
        return 0

    @staticmethod
    def get_encouragement(score):
        """Return positive, motivating reinforcement without shaming."""
        if score >= 88:
            choices = [
                "You're a speech superstar!",
                "Incredible work, champion!",
                "You nailed it!",
                "Sensational pronunciation!",
            ]
        elif score >= 70:
            choices = [
                "Wonderful practice! Keep going!",
                "Great job! You're making progress!",
                "So proud of your effort!",
                "You are sounding clearer every day!",
            ]
        elif score >= 50:
            choices = [
                "Nice try! You're getting better!",
                "Good effort! Practice makes progress!",
                "Keep it up, you're doing great!",
                "Step by step, you're learning!",
            ]
        else:
            choices = [
                "Great try! Every practice counts!",
                "You're learning! That's what matters!",
                "Let's try again together — you've got this!",
                "High five for giving it a go!",
            ]
        return random.choice(choices)

    @staticmethod
    def check_badges(child_id):
        """
        Evaluate badge criteria and award new badges using Django ORM.
        Returns list of newly awarded badge dictionaries.
        """
        from core.models import PracticeSession, Badge

        new_badges = []
        existing_types = set(
            Badge.objects.filter(child_id=child_id).values_list('badge_type', flat=True)
        )

        total_sessions = PracticeSession.objects.filter(child_id=child_id).count()
        high_scores    = PracticeSession.objects.filter(child_id=child_id, score__gte=88).count()

        criteria = [
            ("first_words",    "First Words",        total_sessions >= 1),
            ("practice_pro",   "Practice Pro",       total_sessions >= 10),
            ("super_speaker",  "Super Speaker",      total_sessions >= 25),
            ("star_collector", "Star Collector",     high_scores >= 5),
            ("superstar",      "Shining Superstar",  high_scores >= 15),
        ]

        for badge_type, badge_name, condition in criteria:
            if condition and badge_type not in existing_types:
                badge = Badge.objects.create(
                    child_id=child_id,
                    badge_type=badge_type,
                    badge_name=badge_name,
                )
                new_badges.append(badge)

        return [b.to_dict() for b in new_badges]

    @staticmethod
    def get_level(total_stars):
        """Convert total star count to game level."""
        if total_stars >= 100:
            return 5
        elif total_stars >= 60:
            return 4
        elif total_stars >= 30:
            return 3
        elif total_stars >= 10:
            return 2
        return 1

    @staticmethod
    def get_daily_quest(language='english'):
        """Generate a thematic daily speech challenge."""
        from datetime import datetime
        day_of_year = datetime.now().timetuple().tm_yday
        themes = [
            ("Jungle Adventure", "Find animal sounds and roar with pride!"),
            ("Space Mission",    "Launch into speech galaxy with clear words!"),
            ("Ocean Explorer",   "Dive deep to find magical speech pearls!"),
            ("Magic Garden",     "Water the flower of speech with pronunciation!"),
            ("Mountain Climb",   "Reach the speech summit one word at a time!"),
            ("Castle Quest",     "Unlock the castle gate with clear syllables!"),
            ("Sky Journey",      "Fly high across speech clouds!"),
        ]
        quest_name, quest_desc = themes[day_of_year % len(themes)]
        return {
            'quest_name':        quest_name,
            'quest_description': quest_desc,
            'reward_stars':      5,
        }
