import asyncio
import logging
import time

from django.dispatch import receiver
from django.db.models.signals import post_save
from admin_panel.producer import save_notification_to_rabbitmq

logger = logging.getLogger('logger')


@receiver(post_save, sender='admin_panel.UsersNotification')
def user_saved(sender, instance, created, **kwargs):
    if created is False or sender.is_correct_contacts is False:
        return
    if instance.notification.users_notifications.count() > 100:
        time.sleep(0.1)
    try:
        asyncio.run(
            save_notification_to_rabbitmq(
                {
                    'notification_id': instance.id,
                    'content_id': str(instance.notification.content_id),
                    'is_express': instance.notification.is_express
                }
            )
        )
        logger.info(
            'Sent notification to rabbitmq: {notification_id}'.format(
                notification_id=instance.id
            )
        )
    except Exception as error:
        instance.is_sent_to_queue = False
        instance.save()
        logger.error(
            'Did not sent notification to rabbitmq: {error}'.format(
                error=error
            )
        )
