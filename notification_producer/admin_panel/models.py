from django.contrib.auth import get_user_model
from django.contrib import admin
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CreateUpdate(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Notification(CreateUpdate):
    class Type(models.TextChoices):
        MAIL = "MAIL", _("Почтовая рассылка")

    type = models.CharField(
        choices=Type.choices,
        max_length=40,
        verbose_name="Тип уведомления",
        help_text="Выберите тип уведомления",
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

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return self.type

    # def save(self, *args, **kwargs):
    #     self.author = User.objects.get(username=admin.site.name)
    #     super(Notification, self).save(*args, **kwargs)


class UsersNotification(CreateUpdate):

    user_id = models.UUIDField(
        null=True,
        verbose_name="Пользователь",
        help_text="Укажите id пользователя",
    )
    content_id = models.UUIDField(
        null=True,
        verbose_name="Контент",
        help_text="Укажите id контента",
    )
    notification_id = models.ForeignKey(
        Notification,
        on_delete=models.DO_NOTHING,
        verbose_name="Уведомление",
        help_text="Укажите id уведомления",
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Уведомление пользователя"
        verbose_name_plural = "Уведомления пользователей"

    def __str__(self):
        return str(self.user_id)


class NotificationFrequency(CreateUpdate):
    type = models.SlugField(
        max_length=40,
        verbose_name="Тип уведомления",
        help_text="Выберите тип уведомления",
    )
    frequency = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Периодичность отправки уведомления в минутах",
        help_text="Выберите тип уведомления",
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Периодичность уведомлений"
        verbose_name_plural = "Периодичности уведомлений"

    def __str__(self):
        return self.type
