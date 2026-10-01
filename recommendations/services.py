from django.db import transaction

from activity.models import ActivityType, UserActivity
from .models import Recommendation, Track


class RecommendationService:

    GENRE_WEIGHT = 40
    ARTIST_WEIGHT = 30
    MOOD_WEIGHT = 20
    POPULARITY_WEIGHT = 10

    LIKE_WEIGHT = 25
    COMPLETE_WEIGHT = 15
    SKIP_PENALTY = 30

    def get_recommendations(self, user, limit=10):

        preferences = user.preferences

        tracks = Track.objects.all()

        activity_data = self._get_activity_data(user)

        genres = self._normalize(
            preferences.get("genres", [])
        )

        artists = self._normalize(
            preferences.get("artists", [])
        )

        moods = self._normalize(
            preferences.get("moods", [])
        )

        scored_tracks = []

        for track in tracks:

            score = self._calculate_score(
                track=track,
                genres=genres,
                artists=artists,
                moods=moods,
                activity_data=activity_data,
            )

            if score > 0:

                scored_tracks.append(
                    {
                        "track": track,
                        "score": score,
                    }
                )

        scored_tracks.sort(
            key=lambda item: (
                item["score"],
                item["track"].popularity,
            ),
            reverse=True,
        )

        return scored_tracks[:limit]

    def _calculate_score(
        self,
        track,
        genres,
        artists,
        moods,
        activity_data,
    ):

        score = 0

        has_preference_match = False

        if track.genre.lower() in genres:

            score += self.GENRE_WEIGHT

            has_preference_match = True

        if track.artist_name.lower() in artists:

            score += self.ARTIST_WEIGHT

            has_preference_match = True

        if track.mood.lower() in moods:

            score += self.MOOD_WEIGHT

            has_preference_match = True

        if has_preference_match:

            score += self._popularity_score(
                track.popularity
            )

        # Activity-based scoring

        if track.id in activity_data["liked_tracks"]:

            score += self.LIKE_WEIGHT

        if track.id in activity_data["completed_tracks"]:

            score += self.COMPLETE_WEIGHT

        if track.id in activity_data["skipped_tracks"]:

            score -= self.SKIP_PENALTY

        return max(score, 0)

    def _get_activity_data(self, user):

        activities = (
            UserActivity.objects
            .filter(user=user)
            .values(
                "track_id",
                "activity_type",
            )
        )

        data = {
            "liked_tracks": set(),
            "completed_tracks": set(),
            "skipped_tracks": set(),
        }

        for activity in activities:

            track_id = activity["track_id"]
            activity_type = activity["activity_type"]

            if activity_type == ActivityType.LIKE:

                data["liked_tracks"].add(track_id)

            elif activity_type == ActivityType.COMPLETE:

                data["completed_tracks"].add(track_id)

            elif activity_type == ActivityType.SKIP:

                data["skipped_tracks"].add(track_id)

        return data

    @staticmethod
    def _popularity_score(popularity):

        if popularity >= 90:
            return RecommendationService.POPULARITY_WEIGHT

        if popularity >= 70:
            return 5

        return 0

    @staticmethod
    def _normalize(values):

        return {
            value.strip().lower()
            for value in values
            if isinstance(value, str)
            and value.strip()
        }

    @transaction.atomic
    def generate_and_save_recommendations(
        self,
        user,
        limit=10,
    ):

        recommendations = self.get_recommendations(
            user=user,
            limit=limit,
        )

        Recommendation.objects.filter(
            user=user
        ).delete()

        recommendation_objects = [
            Recommendation(
                user=user,
                track=item["track"],
                score=item["score"],
            )
            for item in recommendations
        ]

        Recommendation.objects.bulk_create(
            recommendation_objects
        )

        return (
            Recommendation.objects
            .filter(user=user)
            .select_related("track")
        )