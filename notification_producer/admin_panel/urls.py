from rest_framework.routers import DefaultRouter

from admin_panel.views.notifications import (
    NotificationCreateAPI, UsersNotificationAPI
)
from admin_panel.views.unsubscribe import (
    UnsubscribeCreateAPI, UnsubscribeDestroyAPI
)
from django.urls import include, path

router = DefaultRouter()
router.register(
    r"notifications", NotificationCreateAPI, basename="notifications"
)
router.register(
    r"users_notifications", UsersNotificationAPI, basename="users_notifications"
)



project_urls = [
    path("", include(router.urls)),
]

notifications_urls = [
    path("", include(router.urls)),
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
