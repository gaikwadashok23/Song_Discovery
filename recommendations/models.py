from django.db import models
from django.conf import settings


class Track(models.Model):
    spotify_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    mood = models.CharField(max_length=100)
    popularity = models.PositiveIntegerField(default=0)

    preview_url = models.URLField(
        null=True,
        blank=True,
    )

    external_url = models.URLField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-popularity"]

    def __str__(self):
        return f"{self.name} - {self.artist_name}"
    
    

class Recommendation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recommendations",
    )

    track = models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
        related_name="recommendations",
    )

    score = models.PositiveIntegerField()

    generated_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-score", "-generated_at"]

    def __str__(self):
        return f"{self.user.email} -> {self.track.name}"