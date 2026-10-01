from django.db.models import Count, Q

from activity.models import ActivityType, UserActivity


class AnalyticsService:

    @staticmethod
    def get_user_summary(user_id):

        activities = UserActivity.objects.filter(
            user_id=user_id
        )

        summary = activities.aggregate(
            total_plays=Count(
                "id",
                filter=Q(
                    activity_type=ActivityType.PLAY
                ),
            ),

            total_likes=Count(
                "id",
                filter=Q(
                    activity_type=ActivityType.LIKE
                ),
            ),

            total_skips=Count(
                "id",
                filter=Q(
                    activity_type=ActivityType.SKIP
                ),
            ),

            total_completions=Count(
                "id",
                filter=Q(
                    activity_type=ActivityType.COMPLETE
                ),
            ),

            unique_tracks_played=Count(
                "track",
                distinct=True,
                filter=Q(
                    activity_type=ActivityType.PLAY
                ),
            ),
        )

        return summary

    @staticmethod
    def get_daily_analytics(user_id):

        return (
            UserActivity.objects
            .filter(user_id=user_id)
            .values("created_at__date")
            .annotate(
                play_count=Count(
                    "id",
                    filter=Q(
                        activity_type=ActivityType.PLAY
                    ),
                ),
                like_count=Count(
                    "id",
                    filter=Q(
                        activity_type=ActivityType.LIKE
                    ),
                ),
                skip_count=Count(
                    "id",
                    filter=Q(
                        activity_type=ActivityType.SKIP
                    ),
                ),
                complete_count=Count(
                    "id",
                    filter=Q(
                        activity_type=ActivityType.COMPLETE
                    ),
                ),
                unique_tracks_played=Count(
                    "track",
                    distinct=True,
                    filter=Q(
                        activity_type=ActivityType.PLAY
                    ),
                ),
            )
            .order_by("-created_at__date")
        )

    @staticmethod
    def get_most_played_tracks(
        user_id,
        limit=10,
    ):

        return (
            UserActivity.objects
            .filter(
                user_id=user_id,
                activity_type=ActivityType.PLAY,
            )
            .values(
                "track_id",
                "track__name",
                "track__artist_name",
            )
            .annotate(
                play_count=Count("id")
            )
            .order_by("-play_count")[:limit]
        )

    @staticmethod
    def get_overall_summary():

        activities = UserActivity.objects.all()

        return {
            "total_activities": activities.count(),

            "total_users": activities.values(
                "user_id"
            ).distinct().count(),

            "total_tracks": activities.values(
                "track_id"
            ).distinct().count(),

            "total_plays": activities.filter(
                activity_type=ActivityType.PLAY
            ).count(),

            "total_likes": activities.filter(
                activity_type=ActivityType.LIKE
            ).count(),

            "total_skips": activities.filter(
                activity_type=ActivityType.SKIP
            ).count(),

            "total_completions": activities.filter(
                activity_type=ActivityType.COMPLETE
            ).count(),
        }
    
    @staticmethod
    def get_trending_data(limit=10):
        trending_genres = (
            UserActivity.objects
            .filter(activity_type=ActivityType.PLAY)
            .values("track__genre")
            .annotate(play_count=Count("id"))
            .order_by("-play_count")[:limit]
        )

        trending_artists = (
            UserActivity.objects
            .filter(activity_type=ActivityType.PLAY)
            .values("track__artist_name")
            .annotate(play_count=Count("id"))
            .order_by("-play_count")[:limit]
        )

        return {
            "genres": [
                {
                    "genre": item["track__genre"],
                    "play_count": item["play_count"],
                }
                for item in trending_genres
            ],
            "artists": [
                {
                    "artist": item["track__artist_name"],
                    "play_count": item["play_count"],
                }
                for item in trending_artists
            ],
        }