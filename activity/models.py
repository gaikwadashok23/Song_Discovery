from django.conf import settings
from django.db import models


class ActivityType(models.TextChoices):
    PLAY = "PLAY", "Play"
    LIKE = "LIKE", "Like"
    SKIP = "SKIP", "Skip"
    COMPLETE = "COMPLETE", "Complete"


class UserActivity(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activities",
    )

    track = models.ForeignKey(
        "recommendations.Track",
        on_delete=models.CASCADE,
        related_name="activities",
    )

    activity_type = models.CharField(
        max_length=20,
        choices=ActivityType.choices,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["user", "-created_at"],
                name="activity_user_time_idx",
            ),
            models.Index(
                fields=["track", "activity_type"],
                name="activity_track_type_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.user.email} - "
            f"{self.track.name} - "
            f"{self.activity_type}"
        )