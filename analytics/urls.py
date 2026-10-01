from django.urls import path

from .views import *


urlpatterns = [

    path(
        "summary/",
        UserAnalyticsSummaryView.as_view(),
        name="user-analytics-summary",
    ),

    path(
        "daily/",
        UserDailyAnalyticsView.as_view(),
        name="user-daily-analytics",
    ),

    path(
        "most-played/",
        MostPlayedTracksView.as_view(),
        name="most-played-tracks",
    ),

    path(
        "overall/",
        OverallAnalyticsView.as_view(),
        name="overall-analytics",
    ),
    
    path(
        "trends/",
        AnalyticsTrendsView.as_view(),
        name="analytics-trends",
    ),
]