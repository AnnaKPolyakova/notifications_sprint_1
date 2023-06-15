from admin_panel.models import UsersUnsubscribe
from rest_framework import serializers


class UnsubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersUnsubscribe
        fields = (
            "user_id",
        )
