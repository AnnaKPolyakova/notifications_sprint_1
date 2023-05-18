from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth import get_user_model

from admin_panel.models import Notification, UsersNotification, \
    NotificationFrequency

User = get_user_model()


@register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = ("type", "author", "text",)
    list_filter = ("type", "author",)
    readonly_fields = ("author",)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@register(UsersNotification)
class UsersNotificationAdmin(admin.ModelAdmin):

    list_display = ("user_id", "content_id", "notification_id",)
    list_filter = ("user_id", "content_id", "notification_id",)


@register(NotificationFrequency)
class NotificationFrequencyAdmin(admin.ModelAdmin):

    list_display = ("type", "frequency",)
    list_filter = ("type", "frequency",)
