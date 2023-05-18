import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


BASE_DIR = Path(__file__).resolve().resolve()

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"), override=True)


class NotificationConsumerSettings(BaseSettings):
    rabbitmq_default_user: str = Field(
        env="RABBITMQ_DEFAULT_USER", default='guest'
    )
    rabbitmq_default_pass: str = Field(
        env="RABBITMQ_DEFAULT_PASS", default='guest'
    )
    rabbitmq_host: str = Field(
        env="RABBITMQ_HOST", default='localhost'
    )
    rabbitmq_notification_routing_key: str = Field(
        env="RABBITMQ_NOTIFICATION_ROUTING_KEY", default='notification'
    )
    rabbitmq_notification_topic: str = Field(
        env="RABBITMQ_NOTIFICATION_TOPIC", default='notification_topic'
    )
    auth_host: str = Field(
        env="AUTH_HOST",
        default="http://127.0.0.1:8001/api/v1/users/auth_check/"
    )
    jwt_secret_key: str = Field(
        env="JWT_SECRET_KEY",
        default="Y0QMIGwksa5OhtOBF9BczuAJ0hYMUv7esEBgMMdAuJ4V7stwxT9e"
    )

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


notification_consumer_settings = NotificationConsumerSettings()
