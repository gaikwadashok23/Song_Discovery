from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .services import *


class UserAnalyticsSummaryView(APIView):

    def get(self, request):

        user_id = request.query_params.get("user")

        if not user_id:
            return Response(
                {
                    "error": "user query parameter is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        summary = AnalyticsService.get_user_summary(
            user_id=user_id
        )

        serializer = AnalyticsSummarySerializer(
            summary
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class UserDailyAnalyticsView(APIView):

    def get(self, request):

        user_id = request.query_params.get("user")

        if not user_id:
            return Response(
                {
                    "error": "user query parameter is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        analytics = (
            AnalyticsService.get_daily_analytics(
                user_id=user_id
            )
        )

        return Response(
            {
                "count": len(analytics),
                "results": analytics,
            },
            status=status.HTTP_200_OK,
        )


class MostPlayedTracksView(APIView):

    def get(self, request):

        user_id = request.query_params.get("user")

        if not user_id:
            return Response(
                {
                    "error": "user query parameter is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        tracks = (
            AnalyticsService.get_most_played_tracks(
                user_id=user_id
            )
        )

        return Response(
            {
                "count": len(tracks),
                "results": tracks,
            },
            status=status.HTTP_200_OK,
        )


class OverallAnalyticsView(APIView):

    def get(self, request):

        summary = (
            AnalyticsService.get_overall_summary()
        )

        return Response(
            summary,
            status=status.HTTP_200_OK,
        )
        
        
class AnalyticsTrendsView(APIView):

    def get(self, request):
        try:
            limit = int(request.query_params.get("limit", 10))

            if limit < 1 or limit > 50:
                return Response(
                    {
                        "error": "limit must be between 1 and 50."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            trends = AnalyticsService.get_trending_data(
                limit=limit
            )

            serializer = AnalyticsTrendsSerializer(
                trends
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        except ValueError:
            return Response(
                {
                    "error": "limit must be a valid integer."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )