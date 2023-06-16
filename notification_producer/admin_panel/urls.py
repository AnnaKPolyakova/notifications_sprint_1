from rest_framework.routers import DefaultRouter
from admin_panel.views.notifications import (
    NotificationCreateAPI, UsersNotificationAPI
)
from admin_panel.views.unsubscribe import (
    UnsubscribeCreateAPI, UnsubscribeDestroyAPI
)
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(
    r"users_notifications",
    UsersNotificationAPI,
    basename="users_notifications"
)


project_urls = [
    path("", include(router.urls)),
]

notifications_urls = [
    path("", include(router.urls)),
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


user_token_urls = [
    path(
        'user_token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'user_token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]

urlpatterns = [
    path("v1/", include(notifications_urls)),
    path("v1/", include(user_token_urls)),
]
