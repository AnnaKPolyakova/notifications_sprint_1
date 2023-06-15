from admin_panel.views.notifications import NotificationCreateAPI
from admin_panel.views.unsubscribe import (
    UnsubscribeCreateAPI, UnsubscribeDestroyAPI
)
from django.urls import include, path

notifications_urls = [
    path(
        "notifications/",
        NotificationCreateAPI.as_view(),
        name="notifications",
    ),
    path(
        "unsubscribes/",
        UnsubscribeCreateAPI.as_view(),
        name="unsubscribes",
    ),
    path(
        "unsubscribes/<uuid:user_id>/",
        UnsubscribeDestroyAPI.as_view(),
        name="unsubscribes-dell",
    ),
]

urlpatterns = [
    path("v1/", include(notifications_urls)),
]
