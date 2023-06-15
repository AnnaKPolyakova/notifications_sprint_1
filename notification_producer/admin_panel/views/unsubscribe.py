from admin_panel.models import UsersUnsubscribe
from admin_panel.serializers.unsubscribe import UnsubscribeSerializer
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response


class UnsubscribeCreateAPI(
    CreateAPIView,
):
    serializer_class = UnsubscribeSerializer


class UnsubscribeDestroyAPI(
    DestroyAPIView
):
    queryset = UsersUnsubscribe
    serializer_class = UnsubscribeSerializer

    def delete(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        if UsersUnsubscribe.objects.filter(user_id=user_id).exists():
            UsersUnsubscribe.objects.get(user_id=user_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
