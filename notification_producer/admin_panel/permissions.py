from http import HTTPStatus

import requests
from rest_framework.permissions import BasePermission

from admin_panel.models import Application
from config import settings


class IsUserAuthenticated(BasePermission):
    """Allows access only to authenticated users."""
    def has_permission(self, request, view):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if token is None:
            return False
        response = getattr(requests, "get")(
            settings.AUTH_HOST,
            headers={"Authorization": 'Bearer {token}'.format(token=token)},
        )
        if response.status_code == HTTPStatus.OK:
            return True
        return False


class IsAppAuthenticated(BasePermission):
    """Allows access only to authenticated users."""
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated) is True:
            return True
        authorization_info = request.META.get(
            'HTTP_AUTHORIZATION', ''
        ).split(' ')
        if len(authorization_info) != 2:
            return False
        try:
            application = Application.objects.get(slug=authorization_info[0])
        except Exception:
            return False
        return application.check_password(authorization_info[1])
