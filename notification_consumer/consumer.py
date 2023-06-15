import asyncio
import json

import aiohttp
from aio_pika import IncomingMessage, connect

from notification_consumer.db import DatabaseManager, engine
from notification_consumer.notification_service import NotificationService
from notification_consumer.settings import (
    notification_consumer_settings as settings
)
from notification_consumer.utils import consumer_logger

QUEUES_AND_PRIORITIES = {
    settings.rabbitmq_notification_queue: 1,
    settings.rabbitmq_notification_express_queue: 2
}


async def save_message(message: IncomingMessage):
    async with message.process():
        data = json.loads(message.body.decode('utf-8'))
        consumer_logger.info(
            " [x] {key}: {data}".format(key=message.routing_key, data=data)
        )
        with DatabaseManager(engine) as session:
            notification_id = data.get('notification_id', None)
            notificator = NotificationService(session, notification_id)
            await notificator.sent_messages()


async def notification_consumers(channel) -> None:
    await channel.set_qos(prefetch_count=1)
    consumer_logger.info("Waiting for messages. To exit press CTRL+C")
    for queue_name in QUEUES_AND_PRIORITIES.keys():
        # Объявите очереди
        queue = await channel.get_queue(queue_name)
        # Начните слушать очереди
        await queue.consume(save_message)


async def get_consumer_count(queue_name):
    api_url = (
        'http://{username}:{password}@{host}:{port}/api/'
        'queues/%2F/{queue_name}'.format(
            username=settings.rabbitmq_default_user,
            password=settings.rabbitmq_default_pass,
            host=settings.rabbitmq_host,
            port=settings.rabbitmq_port,
            queue_name=queue_name,
        )
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            while True:
                if response.status == 200:
                    data_json = await response.json()
                    consumer_count = data_json["consumers"]
                    consumer_logger.info(
                        'consumer_count: {count}'.format(count=consumer_count)
                    )
                    return consumer_count


async def get_num_consumers():
    express_notification_queue_consumers_count = await get_consumer_count(
        settings.rabbitmq_notification_queue
    )
    notification_queue_consumers_count = await get_consumer_count(
        settings.rabbitmq_notification_express_queue
    )
    return max(
        settings.number_of_consumers - max(
            express_notification_queue_consumers_count,
            notification_queue_consumers_count
        ), settings.min_number_of_consumers
    )


async def run_consumers():
    connection = await connect(
        "amqp://{user}:{password}@{host}/".format(
            user=settings.rabbitmq_default_user,
            password=settings.rabbitmq_default_pass,
            host=settings.rabbitmq_host
        )
    )
    channel = await connection.channel()
    consumers = []
    num_consumers = await get_num_consumers()
    consumer_logger.info(
        "num_consumers: {num_consumers}".format(num_consumers=num_consumers)
    )
    for _ in range(num_consumers):
        consumer_task = asyncio.create_task(notification_consumers(channel))
        consumers.append(consumer_task)

    await asyncio.gather(*consumers)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_consumers())
    loop.run_forever()
