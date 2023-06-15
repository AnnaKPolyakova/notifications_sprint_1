import asyncio
import time

from admin_panel.models import NotificationFrequency, UsersNotification
from admin_panel.producer import save_notification_to_rabbitmq
from celery.utils.log import get_task_logger
from schedule.celery_app import app
from schedule.user_notification_creator import UsersNotificationsCreator

logger = get_task_logger(__name__)


@app.task()
def send_notifications(slug):
    logger.info('Start sent_notifications for {slug}'.format(slug=slug))
    if not NotificationFrequency.objects.filter(slug=slug).exists():
        logger.info('NotificationFrequency {slug} not exist'.format(slug=slug))
        return
    frequency = NotificationFrequency.objects.get(slug=slug)
    creator = UsersNotificationsCreator(frequency=frequency)
    creator.create_and_send_users_notifications()
    logger.info('Finished sent_notifications for {slug}'.format(slug=slug))


@app.task()
def save_missing_users_notifications_to_rabbitmq():
    logger.info('Start save_missing_notifications_to_rabbitmq')
    users_notifications = UsersNotification.objects.filter(
        is_sent_to_queue=False,
        is_user_subscribed=True,
    ).order_by('notification__is_express', 'created_at')
    for users_notification in users_notifications:
        time.sleep(0.5)
        logger.info(
            'Users_notification: {users_notification}'.format(
                users_notification=users_notification
            )
        )
        try:
            asyncio.run(
                save_notification_to_rabbitmq(
                    {
                        'notification_id': users_notification.id,
                        'content_id': str(
                            users_notification.notification.content_id
                        ),
                        'is_express':
                            users_notification.notification.is_express
                    }
                )
            )
        except Exception as error:
            logger.error(
                'Did not sent notification to rabbitmq: {error}'.format(
                    error=error
                )
            )
        else:
            users_notification.is_sent_to_queue = True
            super(UsersNotification, users_notification).save()
            logger.info(
                'Users_notification {users_notification} sent to '
                'RabbitMQ'.format(
                    users_notification=users_notification
                )
            )
    logger.info('Finished save_missing_notifications_to_rabbitmq')
