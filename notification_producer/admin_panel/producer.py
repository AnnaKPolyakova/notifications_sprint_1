import asyncio
import json
import logging

from aio_pika import DeliveryMode, Message, connect
from config import settings

logger = logging.getLogger('logger')


async def save_notification_to_rabbitmq(info: dict) -> None:
    # Perform connection
    connection = await connect(
        "amqp://{user}:{password}@{host}/".format(
            user=settings.RABBITMQ_DEFAULT_USER,
            password=settings.RABBITMQ_DEFAULT_PASS,
            host=settings.RABBITMQ_HOST
        )
    )
    async with connection:
        # Creating a channel
        channel = await connection.channel()
        message = Message(
            json.dumps(info).encode('utf-8'),
            delivery_mode=DeliveryMode.PERSISTENT,
        )
        if info.get('is_express', False) is False:
            queue_name = settings.RABBITMQ_NOTIFICATION_QUEUE
            priority = 1
        else:
            queue_name = settings.RABBITMQ_NOTIFICATION_EXPRESS_QUEUE
            priority = 2
        await channel.declare_queue(
            queue_name, durable=True, arguments={'x-max-priority': priority}
        )
        # Sending the message
        await channel.default_exchange.publish(
            message, routing_key=queue_name,
        )
        logger.info("Sent {message}".format(message=message))


if __name__ == "__main__":
    asyncio.run(save_notification_to_rabbitmq({'notification_id': 1}))
