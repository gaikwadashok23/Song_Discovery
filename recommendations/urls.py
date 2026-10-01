from django.urls import path

from .views import (
    RecommendationListView,
    RecommendationRefreshView,
    RecommendationTaskStatusView
)


urlpatterns = [
    path(
        "<uuid:user_id>/refresh/",
        RecommendationRefreshView.as_view(),
        name="recommendation-refresh",
    ),
    path(
        "<uuid:user_id>/",
        RecommendationListView.as_view(),
        name="recommendation-list",
    ),
    
    path(
    "recommendations/tasks/<str:task_id>/",
    RecommendationTaskStatusView.as_view(),
),
]