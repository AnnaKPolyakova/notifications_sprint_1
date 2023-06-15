from django.contrib.admin import ModelAdmin, StackedInline, register
from django.contrib.auth import get_user_model
from admin_panel.models import (
    Notification, NotificationFrequency, UsersNotification
)

User = get_user_model()


class UsersNotificationInline(StackedInline):
    model = UsersNotification
    verbose_name_plural = "Уведомления пользователей"
    fields = ("user_id", "notification", "is_user_subscribed")

    def get_readonly_fields(self, request, obj):
        if obj:
            return "user_id", "is_user_subscribed", "is_sent_to_queue"
        return "is_user_subscribed", "is_sent_to_queue"


@register(Notification)
class NotificationAdmin(ModelAdmin):

    list_display = ('id', "type", "author", "text")
    list_filter = ("type", "author")
    readonly_fields = ("author",)
    inlines = (UsersNotificationInline,)


@register(UsersNotification)
class UsersNotificationAdmin(ModelAdmin):

    list_display = ("id", "user_id", "notification_id")
    list_filter = ("user_id", "notification_id")
    readonly_fields = ("email", "is_user_subscribed", "is_sent_to_queue")


@register(NotificationFrequency)
class NotificationFrequencyAdmin(ModelAdmin):

    list_display = ("slug", "frequency", "notification_id")
    list_filter = ("slug", "frequency", "notification_id")
