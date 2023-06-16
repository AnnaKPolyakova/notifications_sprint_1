import asyncio
import logging

from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from config import settings

logger = logging.getLogger(__name__)

User = get_user_model()


class CreateUpdate(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created_at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated_at"),
    )

    class Meta:
        abstract = True


class Create(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created_at"),
    )

    class Meta:
        abstract = True


class Notification(CreateUpdate):
    class Type(models.TextChoices):
        MAIL = "mail", _("mail")
        REGULAR_MAIL = "regular_mail", _("regular_mail")

    type = models.CharField(
        choices=Type.choices,
        max_length=40,
        verbose_name=_("notification_type"),
        help_text=_("Select notification type"),
    )
    is_express = models.BooleanField(
        default=False,
        verbose_name=_("Field indicating the urgency of the notification"),
        help_text=_("Choose if you need to notify everyone urgently"),
    )

    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        verbose_name=_("The administrator who created the notification"),
        help_text=_("The administrator who created the notification"),
    )
    text = models.TextField(
        max_length=400,
        verbose_name=_("Text notification"),
        help_text=_("Text notification"),
    )
    title = models.CharField(
        max_length=100,
        verbose_name=_("Notice title"),
        help_text=_("Notice title"),
    )
    content_id = models.UUIDField(
        null=True,
        verbose_name=_("content id"),
        help_text=_("set content id"),
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")

    def __str__(self):
        return "{id}, {title}, {type}".format(
            id=self.id, title=self.title, type=self.type
        )


class UsersNotification(CreateUpdate):

    user_id = models.UUIDField(
        null=True,
        verbose_name=_("user id"),
        help_text=_("set user id"),
    )
    notification = models.ForeignKey(
        Notification,
        related_name='users_notifications',
        on_delete=models.DO_NOTHING,
        verbose_name=_("notification"),
        help_text=_("set notification"),
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_("Mail for sending notifications"),
        help_text=_("Mail for sending notifications"),
    )
    is_user_subscribed = models.BooleanField(
        default=True,
        verbose_name=_(
            "A field indicating whether the user is "
            "subscribed to the mailing list"
        ),
        help_text=_(
            "A field indicating whether the user is "
            "subscribed to the mailing list"
        ),
    )
    is_sent_to_queue = models.BooleanField(
        default=True,
        verbose_name=_(
            "A field indicating whether the notifications is queued for "
            "sending"
        )
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = _("users notification")
        verbose_name_plural = _("users notifications")

    def __str__(self):
        return str(self.user_id)

    def save(self, *args, **kwargs):
        if self.id is None:
            if UsersUnsubscribe.objects.filter(user_id=self.user_id).exists:
                self.is_user_unsubscribed = True
            from admin_panel.users_data_getter import UsersDataGetter
            data_getter = UsersDataGetter(self.user_id)
            self.email = asyncio.run(data_getter.get_user_email())
            logger.info(
                "End create_users_messages for {notification}".format(
                    notification=self.id
                )
            )
        super(UsersNotification, self).save(*args, **kwargs)


class NotificationFrequency(CreateUpdate):
    slug = models.SlugField(
        max_length=40,
        verbose_name=_("Unique notification title"),
        help_text=_("Unique notification title"),
    )
    frequency = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_("Notification frequency in seconds"),
        help_text=_("Notification frequency in seconds"),
    )
    users_ids = models.TextField(
        verbose_name=_("List of uuid users to send notifications"),
        help_text=_("List of uuid users to send notifications"),
    )
    notification = models.ForeignKey(
        Notification,
        related_name='frequency',
        on_delete=models.DO_NOTHING,
        verbose_name=_("notification"),
        help_text=_("set notification"),
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = _("notification frequency")
        verbose_name_plural = _("notifications frequencies")

    def __str__(self):
        return self.slug


class UsersUnsubscribe(Create):

    user_id = models.UUIDField(
        null=True,
        verbose_name=_('user'),
        help_text=_('set user'),
        unique=True,
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = _('Opting out of receiving user mailings')
        verbose_name_plural = _('Opting out of receiving user mailings')

    def __str__(self):
        return str(self.user_id)


class Application(Create):

    slug = models.SlugField(
        verbose_name=_('slug'),
        help_text=_('set slug'),
        unique=True,
    )
    password = models.CharField(
        max_length=128,
        verbose_name=_('password'),
        help_text=_('set password'),
    )

    def check_password(self, raw_password):
        return make_password(raw_password, settings.SALT) == self.password

    def save(self, *args, **kwargs):
        self.password = make_password(self.password, settings.SALT)
        super(Application, self).save(*args, **kwargs)

    class Meta:
        ordering = ["created_at"]
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')

    def __str__(self):
        return str(self.slug)
