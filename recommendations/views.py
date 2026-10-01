from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User

from core.cache import (
   
    get_cached_recommendations,
    set_cached_recommendations,
)

from core.throttles import (
    RecommendationThrottle,
    RecommendationAnonThrottle,
)

from .models import Recommendation
from .serializers import RecommendationSerializer

from celery.result import AsyncResult

from .tasks import refresh_user_recommendations



        

class RecommendationRefreshView(APIView):
    
    throttle_classes = [
        RecommendationThrottle,
        RecommendationAnonThrottle,
    ]

    def post(self, request, user_id):

        user = get_object_or_404(
            User,
            id=user_id,
        )

        task = refresh_user_recommendations.delay(
            str(user.id)
        )

        return Response(
            {
                "message": "Recommendation refresh started.",
                "task_id": task.id,
                "user_id": str(user.id),
            },
            status=status.HTTP_202_ACCEPTED,
        )
        
class RecommendationListView(APIView):

    def get(self, request, user_id):

        cached_data = get_cached_recommendations(user_id)

        if cached_data is not None:
            return Response(
                cached_data,
                status=status.HTTP_200_OK,
            )

        user = get_object_or_404(
            User,
            id=user_id,
        )

        recommendations = (
            Recommendation.objects
            .filter(user=user)
            .select_related("track")
        )

        serializer = RecommendationSerializer(
            recommendations,
            many=True,
        )

        response_data = {
            "count": len(recommendations),
            "recommendations": serializer.data,
        }

        set_cached_recommendations(
            user_id,
            response_data,
        )

        return Response(
            response_data,
            status=status.HTTP_200_OK,
        )
        

class RecommendationTaskStatusView(APIView):

    def get(self, request, task_id):

        task = AsyncResult(task_id)

        response_data = {
            "task_id": task_id,
            "status": task.status,
        }

        if task.successful():
            response_data["result"] = task.result

        elif task.failed():
            response_data["error"] = str(task.result)

        return Response(
            response_data,
            status=status.HTTP_200_OK,
        )