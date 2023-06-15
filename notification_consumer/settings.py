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
    rabbitmq_port: int = Field(
        env="RABBITMQ_PORT", default='15672'
    )
    rabbitmq_notification_queue: str = Field(
        env="rabbitmq_notification_queue", default='notification'
    )
    rabbitmq_notification_express_queue: str = Field(
        env="rabbitmq_notification_express_queue",
        default='express_notification'
    )
    jwt_secret_key: str = Field(
        env="JWT_SECRET_KEY",
        default="Y0QMIGwksa5OhtOBF9BczuAJ0hYMUv7esEBgMMdAuJ4V7stwxT9e"
    )
    mail_login: str = Field(
        env="MAIL_LOGIN",
        default="login"
    )
    mail_password: str = Field(
        env="MAIL_PASSWORD",
        default="pass"
    )
    smtp_host: str = Field(
        env="SMTP_HOST",
        default='smtp.yandex.ru'
    )
    smtp_port: int = Field(
        env="SMTP_PORT",
        default=465
    )
    smtp_domain: str = Field(
        env="SMTP_DOMAIN",
        default='yandex.ru'
    )
    postgres_db: str = Field(
        env="POSTGRES_DB",
        default='notification_database'
    )
    postgres_user: str = Field(
        env="POSTGRES_USER",
        default='app'
    )
    postgres_password: str = Field(
        env="POSTGRES_PASSWORD",
        default='123qwe'
    )
    postgres_host: str = Field(
        env="POSTGRES_HOST",
        default='127.0.0.1'
    )
    postgres_port: int = Field(
        env="POSTGRES_PORT",
        default=5432
    )
    number_of_tries_to_get_users: int = Field(
        env="NUMBER_OF_TRIES_TO_GET_USERS",
        default=3
    )
    get_user_info_host: str = Field(
        env="GET_USER_INFO_HOST",
        default="http://127.0.0.1/api/v1/users/{user_id}/"
    )
    number_of_consumers: int = Field(
        env="NUMBER_OF_CONSUMERS",
        default=3
    )
    min_number_of_consumers: int = Field(
        env="MIN_NUMBER_OF_CONSUMERS",
        default=3
    )
    max_number_of_consumers: int = Field(
        env="MAX_NUMBER_OF_CONSUMERS",
        default=10
    )

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


notification_consumer_settings = NotificationConsumerSettings()
