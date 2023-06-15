import asyncio
import logging
import time

from admin_panel.producer import save_notification_to_rabbitmq
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

User = get_user_model()


class CreateUpdate(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Create(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Notification(CreateUpdate):
    class Type(models.TextChoices):
        MAIL = "mail", _("Почтовая рассылка")
        REGULAR_MAIL = "regular_mail", _("Регулярная почтовая рассылка")

    type = models.CharField(
        choices=Type.choices,
        max_length=40,
        verbose_name="Тип уведомления",
        help_text="Выберите тип уведомления",
    )
    is_express = models.BooleanField(
        default=False,
        verbose_name="Поле указывающее на срочность уведомления'",
        help_text="Выберете, если надо уведомить всех срочно",
    )

    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        verbose_name="Администратор создавший уведомление",
        help_text="Администратор создавший уведомление",
    )
    text = models.TextField(
        max_length=400,
        verbose_name="Текст уведомление",
        help_text="Текст уведомления",
    )
    title = models.CharField(
        max_length=100,
        verbose_name="Заголовок уведомление",
        help_text="Заголовок уведомления",
    )
    content_id = models.UUIDField(
        null=True,
        verbose_name="Контент",
        help_text="Укажите id контента",
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return "{id}, {title}, {type}".format(
            id=self.id, title=self.title, type=self.type
        )


class UsersNotification(CreateUpdate):

    user_id = models.UUIDField(
        null=True,
        verbose_name="Пользователь",
        help_text="Укажите id пользователя",
    )
    notification = models.ForeignKey(
        Notification,
        related_name='users_notifications',
        on_delete=models.DO_NOTHING,
        verbose_name="Уведомление",
        help_text="Укажите id уведомления",
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name="Почта на которую было направлено уведомление",
        help_text="Почта на которую было направлено уведомление",
    )
    is_user_subscribed = models.BooleanField(
        default=True,
        verbose_name="Поле указывающее согласен ли на рассылку пользователь",
        help_text="Поле указывающее согласен ли на рассылку пользователь",
    )
    is_sent_to_queue = models.BooleanField(
        default=True,
        verbose_name="Поле указывающее поставлено ли сообщение в очередь на "
                     "отправку",
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Уведомление пользователя"
        verbose_name_plural = "Уведомления пользователей"

    def __str__(self):
        return str(self.user_id)

    def save(self, *args, **kwargs):
        sent_to_queue = False
        if self.id is None:
            sent_to_queue = True
            if UsersUnsubscribe.objects.filter(user_id=self.user_id).exists:
                self.is_user_unsubscribed = True
                super(UsersNotification, self).save(*args, **kwargs)
            from admin_panel.users_data_getter import UsersDataGetter
            data_getter = UsersDataGetter(self.user_id)
            self.email = asyncio.run(data_getter.get_user_email())
            logger.info(
                "End create_users_messages for {notification}".format(
                    notification=self.id
                )
            )
        super(UsersNotification, self).save(*args, **kwargs)
        if sent_to_queue and self.email:
            if self.notification.users_notifications.count() > 100:
                time.sleep(0.1)
            try:
                asyncio.run(
                    save_notification_to_rabbitmq(
                        {
                            'notification_id': self.id,
                            'content_id': str(self.notification.content_id),
                            'is_express': self.notification.is_express
                        }
                    )
                )
            except Exception as error:
                self.is_sent_to_queue = False
                super(UsersNotification, self).save(*args, **kwargs)
                logger.error(
                    'Did not sent notification to rabbitmq: {error}'.format(
                        error=error
                    )
                )


class NotificationFrequency(CreateUpdate):
    slug = models.SlugField(
        max_length=40,
        verbose_name="Уникальное название уведомления",
        help_text="Уникальное название уведомления",
    )
    frequency = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Периодичность отправки уведомления в секундах",
        help_text="Периодичность отправки уведомления в секундах",
    )
    users_ids = models.TextField(
        verbose_name="Список uuid пользователей для отправки уведомлений",
        help_text="Список uuid пользователей для отправки уведомлений",
    )
    notification = models.ForeignKey(
        Notification,
        related_name='frequency',
        on_delete=models.DO_NOTHING,
        verbose_name="Уведомление",
        help_text="Укажите id уведомления",
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Периодичность уведомлений"
        verbose_name_plural = "Периодичности уведомлений"

    def __str__(self):
        return self.slug


class UsersUnsubscribe(Create):

    user_id = models.UUIDField(
        null=True,
        verbose_name="Пользователь",
        help_text="Укажите id пользователя",
        unique=True,
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Отказ от получения рассылок пользователя"
        verbose_name_plural = "Отказы от получения рассылок пользователей"

    def __str__(self):
        return str(self.user_id)
