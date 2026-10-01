from django.urls import path

from .views import (
    UserActivityCreateView,
    UserActivityListView,
    UserActivitySummaryView,
)


urlpatterns = [
    path(
        "activity-create/",
        UserActivityCreateView.as_view(),
        name="activity-create",
    ),
    path(
        "activity-list/",
        UserActivityListView.as_view(),
        name="activity-list",
        ),
        
    path(
        "summary/",
        UserActivitySummaryView.as_view(),
        name="activity-summary",
    ),
]