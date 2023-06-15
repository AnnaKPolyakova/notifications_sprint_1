import json
import logging
from logging.config import dictConfig

from aio_pika import DeliveryMode, Message, connect

from notification_consumer.settings import (
    notification_consumer_settings as settings
)

dictConfig(
    {
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            },
            'debug-console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
        },
        'loggers': {
            '': {
                'handlers': ['debug-console'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }
)

consumer_logger = logging.getLogger("consumer")


async def save_notification_to_dead_letter_queue(
        info_data: dict, queue_name: str
) -> None:
    consumer_logger.info("Start global save_notification_to_dead_letter_queue")
    connection_rabbitmq = await connect(
        "amqp://{user}:{password}@{host}/".format(
            user=settings.rabbitmq_default_user,
            password=settings.rabbitmq_default_pass,
            host=settings.rabbitmq_host
        )
    )
    async with connection_rabbitmq:
        # Creating a channel
        channel = await connection_rabbitmq.channel()
        message = Message(
            json.dumps(info_data).encode('utf-8'),
            delivery_mode=DeliveryMode.PERSISTENT,
        )
        # Sending the message
        await channel.default_exchange.publish(
            message, routing_key=queue_name,
        )
        consumer_logger.info("Sent {info}".format(info=info_data))
