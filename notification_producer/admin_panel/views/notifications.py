from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from admin_panel.models import UsersNotification
from admin_panel.serializers.notifications import (
    NotificationSerializer,
    UsersNotificationSerializer,
    UsersNotificationDetailSerializer
)

from admin_panel.permissions import IsUserAuthenticated, IsAppAuthenticated


class NotificationCreateAPI(
    CreateAPIView
):
    serializer_class = NotificationSerializer
    permission_classes = (IsAppAuthenticated,)

    def perform_create(self, serializer):
        if self.request.user.is_anonymous is True:
            notification = serializer.save()
        else:
            notification = serializer.save(author=self.request.user)
        users_ids = self.request.data["users"]
        data = [
            {"user_id": user_id, "notification": notification.id} for
            user_id in users_ids
        ]
        users_notification_serializer = UsersNotificationSerializer(
            data=data, many=True
        )
        users_notification_serializer.is_valid(raise_exception=True)
        users_notification_serializer.save()


class UsersNotificationAPI(
    GenericViewSet
):
    serializer_class = UsersNotificationDetailSerializer

    @action(
        methods=["get"],
        detail=False,
        url_path="user/(?P<user_id>[0-9a-f]{32})",
        url_name="user_notifications",
        permission_classes=[IsUserAuthenticated]
    )
    def get_user_notifications(self, request, user_id):
        """Get users notifications"""
        notifications = UsersNotification.objects.filter(
            user_id=user_id,
        ).order_by("created_at")
        page = self.paginate_queryset(notifications)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return self.get_serializer(notifications, many=True)
