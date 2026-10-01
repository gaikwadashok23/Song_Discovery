from rest_framework import serializers

from .models import Recommendation


class RecommendationSerializer(serializers.ModelSerializer):
    track_name = serializers.CharField(
        source="track.name",
        read_only=True,
    )

    artist_name = serializers.CharField(
        source="track.artist_name",
        read_only=True,
    )

    genre = serializers.CharField(
        source="track.genre",
        read_only=True,
    )

    mood = serializers.CharField(
        source="track.mood",
        read_only=True,
    )

    popularity = serializers.IntegerField(
        source="track.popularity",
        read_only=True,
    )

    class Meta:
        model = Recommendation
        fields = [
            "id",
            "track_name",
            "artist_name",
            "genre",
            "mood",
            "popularity",
            "score",
            "generated_at",
        ]