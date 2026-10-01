from celery import shared_task

from recommendations.tasks import (
    refresh_user_recommendations,
)


@shared_task
def refresh_recommendations_after_activity(
    user_id,
):
    task = refresh_user_recommendations.delay(
        user_id
    )

    return {
        "user_id": str(user_id),
        "recommendation_task_id": task.id,
    }