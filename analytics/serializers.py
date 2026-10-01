from rest_framework import serializers

from .models import DailyUserAnalytics


class DailyUserAnalyticsSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = DailyUserAnalytics

        fields = [
            "id",
            "user",
            "date",
            "play_count",
            "like_count",
            "skip_count",
            "complete_count",
            "unique_tracks_played",
            "created_at",
            "updated_at",
        ]

        read_only_fields = fields
        
        
        
class AnalyticsSummarySerializer(
    serializers.Serializer
):
    total_plays = serializers.IntegerField()
    total_likes = serializers.IntegerField()
    total_skips = serializers.IntegerField()
    total_completions = serializers.IntegerField()
    unique_tracks_played = serializers.IntegerField()
    
class TrendingGenreSerializer(serializers.Serializer):
    genre = serializers.CharField()
    play_count = serializers.IntegerField()


class TrendingArtistSerializer(serializers.Serializer):
    artist = serializers.CharField()
    play_count = serializers.IntegerField()


class AnalyticsTrendsSerializer(serializers.Serializer):
    genres = TrendingGenreSerializer(many=True)
    artists = TrendingArtistSerializer(many=True)