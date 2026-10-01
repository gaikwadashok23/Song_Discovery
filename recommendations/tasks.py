from celery import shared_task

from users.models import User
from .services import RecommendationService
from core.cache import delete_cached_recommendations


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def refresh_user_recommendations(self, user_id):

    user = User.objects.get(
        id=user_id
    )

    service = RecommendationService()

    recommendations = (
        service.generate_and_save_recommendations(
            user=user,
            limit=10,
        )
    )

    delete_cached_recommendations(
        user_id
    )

    return {
        "user_id": str(user_id),
        "count": recommendations.count(),
    }
    
@shared_task
def refresh_all_user_recommendations():

    users = (
        User.objects
        .filter(is_active=True)
        .values_list("id", flat=True)
    )

    task_count = 0

    for user_id in users:
        refresh_user_recommendations.delay(str(user_id))
        task_count += 1

    return {
        "message": "Recommendation refresh tasks queued.",
        "users_queued": task_count,
    }