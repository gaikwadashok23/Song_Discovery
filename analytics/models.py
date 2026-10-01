from django.conf import settings
from django.db import models


class DailyUserAnalytics(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="daily_analytics",
    )

    date = models.DateField(
        db_index=True
    )

    play_count = models.PositiveIntegerField(
        default=0
    )

    like_count = models.PositiveIntegerField(
        default=0
    )

    skip_count = models.PositiveIntegerField(
        default=0
    )

    complete_count = models.PositiveIntegerField(
        default=0
    )

    unique_tracks_played = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"],
                name="unique_user_daily_analytics",
            )
        ]

        indexes = [
            models.Index(
                fields=["user", "-date"],
                name="analytics_user_date_idx",
            ),
            models.Index(
                fields=["date"],
                name="analytics_date_idx",
            ),
        ]

        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.email} - {self.date}"