from django.db.models import Count

from .models import ActivityType, UserActivity


class ActivityService:

    @staticmethod
    def get_user_activities(user_id, limit=50):

        return (
            UserActivity.objects
            .filter(user_id=user_id)
            .select_related("track")
            .order_by("-created_at")[:limit]
        )

    @staticmethod
    def get_activity_summary(user_id):

        summary = (
            UserActivity.objects
            .filter(user_id=user_id)
            .values("activity_type")
            .annotate(count=Count("id"))
            .order_by("activity_type")
        )

        result = {
            ActivityType.PLAY: 0,
            ActivityType.LIKE: 0,
            ActivityType.SKIP: 0,
            ActivityType.COMPLETE: 0,
        }

        for item in summary:
            result[item["activity_type"]] = item["count"]

        return result
    
    