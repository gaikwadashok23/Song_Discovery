from django.urls import path

from .views import UserCreateView, UserDetailView


urlpatterns = [
    path(
        "",
        UserCreateView.as_view(),
        name="user-create",
    ),
    path(
        "<uuid:user_id>/",
        UserDetailView.as_view(),
        name="user-detail",
    ),
]