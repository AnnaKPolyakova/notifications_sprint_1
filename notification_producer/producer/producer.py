import asyncio
import logging
import json

from aio_pika import DeliveryMode, ExchangeType, Message, connect

from config import settings


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
        exchange = await channel.declare_exchange(
            settings.RABBITMQ_NOTIFICATION_TOPIC,
            ExchangeType.TOPIC
        )
        message = Message(
            json.dumps(info).encode('utf-8'),
            delivery_mode=DeliveryMode.PERSISTENT,
        )
        # Sending the message
        await exchange.publish(
            message,
            routing_key=settings.RABBITMQ_NOTIFICATION_ROUTING_KEY
        )
        logging.info(f"Sent {message!r}")


if __name__ == "__main__":
    asyncio.run(save_notification_to_rabbitmq(
        {'info': 1}
    ))
    print("done")
