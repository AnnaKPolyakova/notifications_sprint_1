import asyncio
import os
import smtplib
from abc import ABC, abstractmethod
from email.message import EmailMessage
from http import HTTPStatus

import aiohttp
from jinja2 import Environment, FileSystemLoader

from notification_consumer.db import DatabaseManager, engine
from notification_consumer.models import Notification, UsersNotification
from notification_consumer.settings import notification_consumer_settings
from notification_consumer.settings import (
    notification_consumer_settings as settings
)
from notification_consumer.utils import (
    consumer_logger,
    save_notification_to_dead_letter_queue
)


class AbstractNotificationService(ABC):

    @abstractmethod
    async def send_messages(self):
        pass


class MailNotificationService(AbstractNotificationService):
    def __init__(self, session, user_notification, notification):
        self.notification: Notification = notification
        self.session = session
        self.user_notification: UsersNotification = user_notification
        self.username = None
        self.from_email = '{login}@{domain}'.format(
            login=notification_consumer_settings.mail_login,
            domain=notification_consumer_settings.smtp_domain
        )
        self.server: smtplib.SMTP_SSL = smtplib.SMTP_SSL(
            notification_consumer_settings.smtp_host,
            notification_consumer_settings.smtp_port
        )
        self.message = EmailMessage()

    async def _save_notification_to_dead_letter_queue(self):
        if self.notification.is_express is True:
            dead_letter_queue = "{queue_name}_dlq".format(
                queue_name=settings.rabbitmq_notification_express_queue
            )
        else:
            dead_letter_queue = "{queue_name}_dlq".format(
                queue_name=settings.rabbitmq_notification_queue
            )
        await save_notification_to_dead_letter_queue(
            {
                'notification_id': self.user_notification.id,
                'content_id': str(self.notification.content_id),
                "dlq": str(True)
            }, dead_letter_queue
        )

    async def _get_user_info(self):
        consumer_logger.info('Start _get_user_info')
        for _ in range(settings.number_of_tries_to_get_users):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        settings.get_user_info_host.format(
                            user_id=self.user_notification.user_id
                        )
                    ) as response:
                        if response.status != HTTPStatus.OK:
                            continue
                        data = await response.json()
                        consumer_logger.info('Finished _get_user_info')
                        return data.get('login', '')
            except Exception as error:
                consumer_logger.error(error)
        consumer_logger.info(
            '_get_user_info start to _save_notification_to_dead_letter_queue'
        )
        await self._save_notification_to_dead_letter_queue()

    def _prepare_message(self):
        self.message['From'] = self.from_email
        self.message['To'] = [self.user_notification.contact]
        self.message['Subject'] = self.notification.title
        # Указываем расположение шаблонов
        current_path = os.path.dirname(__file__)
        loader = FileSystemLoader(current_path)
        env = Environment(loader=loader)
        # Загружаем нужный шаблон в переменную
        template = env.get_template('notification_template.html')
        # Заполняем шаблон нужной информацией:
        # в метод render передаются данные,
        # которые нужно подставить в шаблон.
        data = {
            'title': self.notification.title,
            'text': self.notification.text,
            'name': self.username
        }
        output = template.render(**data)
        self.message.add_alternative(output, subtype='html')

    async def _sent_messages_for_user(self):
        self.server.login(
            notification_consumer_settings.mail_login,
            notification_consumer_settings.mail_password
        )
        for number_of_tries in range(settings.number_of_tries_to_get_users):
            try:
                self.server.sendmail(
                    self.from_email,
                    [self.user_notification.contact],
                    self.message.as_string()
                )
            except smtplib.SMTPException as exc:
                reason = '{name}: {exc}'.format(
                    name=type(exc).__name__, exc=exc
                )
                consumer_logger.info(
                    'Failed to send email. {reason}'.format(
                        reason=reason
                    )
                )
                if (
                        number_of_tries ==
                        settings.number_of_tries_to_get_users - 1
                ):
                    await self._save_notification_to_dead_letter_queue()
                    consumer_logger.info(
                        'UserNotification {id} saved to dead letter '
                        'queue'.format(id=self.user_notification)
                    )
            else:
                consumer_logger.info(
                    'Letter sent to {mail}'.format(
                        mail=self.user_notification.contact
                    )
                )
            finally:
                self.server.close()
                consumer_logger.info('Done')

    async def send_messages(self):
        if self.user_notification.contact is None:
            consumer_logger.info(
                'Can not get mail for user notification {notification}'.format(
                    notification=self.user_notification.id
                )
            )
            return
        self.username = await self._get_user_info()
        self._prepare_message()
        await self._sent_messages_for_user()


class TelegramNotificationService(AbstractNotificationService):

    async def send_messages(self):
        # TODO
        pass


if __name__ == "__main__":
    with DatabaseManager(engine) as session:
        notificator = MailNotificationService(session, 13, 1)
        asyncio.run(notificator.send_messages())
