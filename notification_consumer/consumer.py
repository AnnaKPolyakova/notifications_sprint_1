import asyncio
import json
import logging
import sys

from aio_pika import ExchangeType, connect
from aio_pika.abc import AbstractIncomingMessage


async def notification_consumer() -> None:
    # Perform connection
    connection = await connect("amqp://guest1:guest1@localhost/")
    # Creating a channel
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    # Declare an exchange
    topic_logs_exchange = await channel.declare_exchange(
        "notification_topic", ExchangeType.TOPIC,
    )
    # Declaring queue
    queue = await channel.declare_queue(
        "notification", durable=True,
    )
    await queue.bind(topic_logs_exchange, routing_key='notification')
    logging.info("Waiting for messages. To exit press CTRL+C")
    # Start listening the queue with name 'task_queue'
    async with queue.iterator() as iterator:
        message: AbstractIncomingMessage
        async for message in iterator:
            async with message.process():
                data = json.loads(message.body.decode('utf-8'))
                print(f" [x] {message.routing_key!r}: {data!r}")


if __name__ == "__main__":
    asyncio.run(notification_consumer())