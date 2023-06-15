from http import HTTPStatus

import requests
from rest_framework.permissions import BasePermission
from config import settings


class IsUserAuthenticated(BasePermission):
    """Allows access only to authenticated users."""
    def has_permission(self, request, view):
        authorization = request.META['HTTP_AUTHORIZATION']
        response = getattr(requests, "get")(
            settings.AUTH_HOST,
            headers={"Authorization": authorization},
        )
        if response.status_code == HTTPStatus.OK:
            return True
        return False
