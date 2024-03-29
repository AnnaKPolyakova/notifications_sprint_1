import os

RABBITMQ_DEFAULT_USER = os.environ.get("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.environ.get("RABBITMQ_DEFAULT_PASS")
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
RABBITMQ_NOTIFICATION_QUEUE = os.environ.get("RABBITMQ_NOTIFICATION_QUEUE")
RABBITMQ_NOTIFICATION_EXPRESS_QUEUE = os.environ.get(
    "RABBITMQ_NOTIFICATION_EXPRESS_QUEUE"
)
