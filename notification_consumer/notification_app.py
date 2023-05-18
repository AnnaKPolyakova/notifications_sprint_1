import asyncio
import logging

from flask import Flask, request
from flask_jwt_extended import JWTManager

from notification_consumer.consumer import notification_consumer
from notification_consumer.settings import notification_consumer_settings
from notification_consumer.utils import init_logging


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        if request:
            record.request_id = request.headers.get("X-Request-Id", "")
        return True


def create_notification_app():
    init_logging()
    current_app = Flask(__name__)
    current_app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    current_app.config["JWT_HEADER_NAME"] = "Authorization"
    current_app.config["JWT_HEADER_TYPE"] = "Bearer"
    current_app.config["JWT_SECRET_KEY"] = \
        notification_consumer_settings.jwt_secret_key
    JWTManager(current_app)
    asyncio.run(notification_consumer())
    return current_app


if __name__ == "__main__":
    app = create_notification_app()
    app.run(port=5000)
