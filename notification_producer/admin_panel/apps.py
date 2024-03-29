from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class AdminPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_panel'
    verbose_name = _("notifications")

    def ready(self):
        import admin_panel.signals  # noqa: F401,WPS301
