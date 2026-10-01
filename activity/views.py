from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *

from .services import *
from .tasks import refresh_recommendations_after_activity


class UserActivityCreateView(APIView):

    def post(self, request):

        serializer = UserActivitySerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        activity = serializer.save()

        refresh_task = (
            refresh_recommendations_after_activity.delay(
                str(activity.user.id)
            )
        )

        return Response(
            {
                "message": "Activity recorded successfully.",
                "activity": UserActivitySerializer(
                    activity
                ).data,
                "recommendation_refresh_task_id": refresh_task.id,
            },
            status=status.HTTP_201_CREATED,
        )


class UserActivityListView(APIView):

    def get(self, request):

        user_id = request.query_params.get("user")

        if not user_id:
            return Response(
                {
                    "error": "user query parameter is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        activities = ActivityService.get_user_activities(
            user_id=user_id,
            limit=50,
        )

        serializer = UserActivitySerializer(
            activities,
            many=True,
        )

        return Response(
            {
                "count": len(serializer.data),
                "activities": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class UserActivitySummaryView(APIView):

    def get(self, request):

        user_id = request.query_params.get("user")

        if not user_id:
            return Response(
                {
                    "error": "user query parameter is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        summary = ActivityService.get_activity_summary(
            user_id=user_id,
        )

        return Response(
            {
                "summary": summary,
            },
            status=status.HTTP_200_OK,
        )
        
        
