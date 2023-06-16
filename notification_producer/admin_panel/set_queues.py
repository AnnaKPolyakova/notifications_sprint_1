import asyncio
import logging

from aio_pika import connect
from config import settings

logger = logging.getLogger('logger')


async def set_queues():
    connection = await connect(
        "amqp://{user}:{password}@{host}/".format(
            user=settings.RABBITMQ_DEFAULT_USER,
            password=settings.RABBITMQ_DEFAULT_PASS,
            host=settings.RABBITMQ_HOST
        )
    )
    async with connection:
        logger.info("Start set queues")
        channel = await connection.channel()
        await channel.declare_queue(
            settings.RABBITMQ_NOTIFICATION_QUEUE,
            durable=True,
            arguments={'x-max-priority': 1}
        )
        args = {
            'x-dead-letter-exchange': '',
            'x-message-ttl': 30000,
            'x-dead-letter-routing-key': settings.RABBITMQ_NOTIFICATION_QUEUE
        }
        await channel.declare_queue(
            settings.RABBITMQ_NOTIFICATION_QUEUE + '_dlq', arguments=args
        )

        await channel.declare_queue(
            settings.RABBITMQ_NOTIFICATION_EXPRESS_QUEUE,
            durable=True,
            arguments={'x-max-priority': 2}
        )
        args = {
            'x-dead-letter-exchange': '',
            'x-message-ttl': 3000,
            'x-dead-letter-routing-key':
                settings.RABBITMQ_NOTIFICATION_EXPRESS_QUEUE
        }
        await channel.declare_queue(
            '{queue}_dlq'.format(
                queue=settings.RABBITMQ_NOTIFICATION_EXPRESS_QUEUE
            ),
            arguments=args
        )
        logger.info("End set queues")


if __name__ == "__main__":
    asyncio.run(set_queues())
