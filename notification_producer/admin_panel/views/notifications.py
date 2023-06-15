from admin_panel.serializers.notifications import (
    NotificationSerializer, UsersNotificationSerializer
)
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated


class NotificationCreateAPI(
    CreateAPIView,
):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        notification = serializer.save(author=self.request.user)
        users_ids = self.request.data["users"]
        data = [
            {"user_id": user_id, "notification": notification.id} for
            user_id in users_ids
        ]
        serializer = UsersNotificationSerializer(
            data=data, many=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
