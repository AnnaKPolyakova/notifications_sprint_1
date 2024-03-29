from admin_panel.models import Notification, UsersNotification
from rest_framework import serializers


class UsersNotificationSerializer(serializers.ModelSerializer):
    notification = serializers.PrimaryKeyRelatedField(
        queryset=Notification.objects.all()
    )

    class Meta:
        model = UsersNotification
        fields = (
            "user_id",
            "notification",
        )


class UsersNotificationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersNotification
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):

    users = serializers.ListField(
        child=serializers.UUIDField(), read_only=True
    )

    class Meta:
        model = Notification
        fields = (
            "type",
            "is_express",
            "text",
            "title",
            "content_id",
            "users"
        )
