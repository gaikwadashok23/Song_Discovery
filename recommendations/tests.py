from django.test import TestCase

# Create your tests here.
from django.core.management import call_command
from django.db import IntegrityError
from django.test import TestCase

from .models import Track
from .services import RecommendationService
from .models import Track, Recommendation

# class RecommendationModelTestCase(TestCase):

#     def setUp(self):
#         from users.models import User

#         self.user = User.objects.create_user(
#             email="ashok@example.com",
#             name="Ashok",
#             password="test123",
#         )

#         self.track = Track.objects.create(
#             spotify_id="recommendation_001",
#             name="Test Song",
#             artist_name="Test Artist",
#             genre="rock",
#             mood="happy",
#             popularity=90,
#         )

#     def test_create_recommendation(self):
#         recommendation = Recommendation.objects.create(
#             user=self.user,
#             track=self.track,
#             score=90,
#         )

#         self.assertEqual(
#             Recommendation.objects.count(),
#             1,
#         )

#         self.assertEqual(
#             recommendation.user,
#             self.user,
#         )

#         self.assertEqual(
#             recommendation.track,
#             self.track,
#         )

#         self.assertEqual(
#             recommendation.score,
#             90,
#         )

#     def test_recommendation_string(self):
#         recommendation = Recommendation.objects.create(
#             user=self.user,
#             track=self.track,
#             score=90,
#         )

#         self.assertEqual(
#             str(recommendation),
#             "ashok@example.com -> Test Song",
#         )

class RecommendationGenerationTestCase(TestCase):

    def setUp(self):
        from users.models import User

        self.user = User.objects.create_user(
            email="generator@example.com",
            name="Generator User",
            password="test123",
            preferences={
                "genres": ["rock"],
                "artists": ["Coldplay"],
                "moods": ["happy"],
            },
        )

        Track.objects.create(
            spotify_id="gen_001",
            name="Happy Rock",
            artist_name="Coldplay",
            genre="rock",
            mood="happy",
            popularity=95,
        )

        Track.objects.create(
            spotify_id="gen_002",
            name="Sad Rock",
            artist_name="Coldplay",
            genre="rock",
            mood="sad",
            popularity=80,
        )

        Track.objects.create(
            spotify_id="gen_003",
            name="Pop Song",
            artist_name="Adele",
            genre="pop",
            mood="sad",
            popularity=95,
        )

        self.service = RecommendationService()

    def test_generate_and_save_recommendations(self):
        recommendations = (
            self.service.generate_and_save_recommendations(
                self.user
            )
        )

        self.assertEqual(
            Recommendation.objects.filter(
                user=self.user
            ).count(),
            2,
        )

        self.assertEqual(
            recommendations[0].track.name,
            "Happy Rock",
        )

        self.assertEqual(
            recommendations[0].score,
            100,
        )