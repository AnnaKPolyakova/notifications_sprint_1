import asyncio
import datetime
from typing import List
from admin_panel.models import (
    Notification, NotificationFrequency, UsersNotification, UsersUnsubscribe
)

from admin_panel.producer import save_notification_to_rabbitmq
from admin_panel.users_data_getter import UsersDataGetter
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class UsersNotificationsCreator:
    def __init__(self, frequency):
        self.notification: Notification = frequency.notification
        self.frequency: NotificationFrequency = frequency
        self.users_ids: List = []
        self.users_notifications = UsersNotification.objects.none()
        self.users_data: dict = {}
        self.users_who_subscribed: list = []
        self.send_to_rabbitmq: bool = True

    def _get_users_ids(self):
        logger.info('Start _get_users_ids')
        users_ids = self.frequency.users_ids
        logger.info(
            'users_ids is {users_ids}'.format(users_ids=users_ids)
        )
        if not isinstance(users_ids, str):
            logger.info(
                'users_ids is not str {users_ids}'.format(users_ids=users_ids)
            )
            return
        users_ids = users_ids.replace(" ", "")
        self.users_ids = list(set(users_ids.split(",")))
        logger.info(
            'users_ids is {users_ids}'.format(users_ids=self.users_ids)
        )

    def _get_users_who_subscribed(self):
        users_who_unsubscribed = UsersUnsubscribe.objects.filter(
            user_id__in=self.users_ids
        ).values_list('user_id')
        logger.info(
            'Unsubscribed users: {users}'.format(users=users_who_unsubscribed)
        )
        result = []
        for user_id in self.users_ids:
            if user_id not in users_who_unsubscribed:
                result.append(user_id)
        self.users_who_subscribed = result
        logger.info(
            'Subscribed users: {users}'.format(users=self.users_who_subscribed)
        )

    def _get_users_data(self):
        logger.info('Start get_user_contact')
        data_getter = UsersDataGetter(
            self.users_who_subscribed, self.notification.TYPES_AND_FIELDS[
                self.notification.type
            ]
        )
        self.users_data = data_getter.get_data_for_users()

    def _create_users_notifications(self):
        logger.info('Start _create_users_notifications')
        users_notifications = []
        self._get_users_who_subscribed()
        self._get_users_data()
        if not isinstance(self.users_data, dict):
            self.send_to_rabbitmq = False
        for user_id in self.users_ids:
            is_correct_contacts = True
            is_user_subscribed = True
            if user_id not in self.users_who_subscribed:
                is_user_subscribed = False
                contact = ''
            elif not isinstance(self.users_data, dict):
                contact = None
            else:
                contact = self.users_data[user_id]
            logger.info('contact: {contact}'.format(contact=contact))
            if contact is False:
                is_correct_contacts = False
            try:
                users_notifications.append(
                    UsersNotification(
                        user_id=user_id,
                        notification=self.notification,
                        contact=contact,
                        is_user_subscribed=is_user_subscribed,
                        created_at=datetime.datetime.now(),
                        updated_at=datetime.datetime.now(),
                        is_correct_contacts=is_correct_contacts
                    )
                )
            except Exception as error:
                logger.info('error: {e}'.format(e=error))
        self.users_notifications = UsersNotification.objects.bulk_create(
            users_notifications, 1000
        )

    def _save_notification_to_rabbitmq(self):
        logger.info(
            'Start _save_notification_to_rabbitmq: {notifications}'.format(
                notifications=self.users_notifications
            )
        )
        for user_notification in self.users_notifications:
            logger.info('user_notification: {user_notification}'.format(
                user_notification=user_notification
            ))
            if (
                    user_notification.is_correct_contacts is False or
                    user_notification.is_user_subscribed is False
            ):
                logger.info(
                    'User_notification does not saved to '
                    'rabbitmq: {user_notification}'.format(
                        user_notification=user_notification
                    )
                )
                logger.info(
                    'is_user_subscribed: {is_user_subscribed}'.format(
                        is_user_subscribed=user_notification.is_user_subscribed
                    )
                )
                logger.info(
                    'is_correct_contacts: {value}'.format(
                        value=user_notification.is_correct_contacts
                    )
                )
                continue
            logger.info('check contact')
            if user_notification.contact:
                asyncio.run(
                    save_notification_to_rabbitmq(
                        {
                            'notification_id': user_notification.id,
                            'content_id': str(self.notification.content_id),
                            'is_express': self.notification.is_express
                        }
                    )
                )
                logger.info(
                    'Save notification {id} to rabbitmq'.format(
                        id=user_notification.id
                    )
                )

    def create_and_send_users_notifications(self):
        logger.info('Start create_and_send_users_notifications')
        self._get_users_ids()
        self._create_users_notifications()
        logger.info('_save_notification_to_rabbitmq')
        if self.send_to_rabbitmq:
            self._save_notification_to_rabbitmq()
            logger.info('Finished create_and_send_users_notifications')
        else:
            logger.info('Finished create_users_notifications only')
