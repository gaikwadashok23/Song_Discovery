from django.core.management.base import BaseCommand
from django_celery_beat.models import (
    IntervalSchedule,
    PeriodicTask,
)


class Command(BaseCommand):

    help = "Create periodic recommendation refresh task"

    def handle(self, *args, **options):

        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.HOURS,
        )

        PeriodicTask.objects.update_or_create(
            name="Refresh all user recommendations",
            defaults={
                "interval": schedule,
                "task": (
                    "recommendations.tasks."
                    "refresh_all_user_recommendations"
                ),
                "enabled": True,
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Periodic task configured successfully."
            )
        )