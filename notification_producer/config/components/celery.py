import os

CELERY_CACHE_BACKEND = 'default'
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timoit": 3600}
CELERY_TIMEZONE = "Europe/Moscow"

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = str(os.environ.get("REDIS_PORT", 6379))
REDIS_PROTOCOL = os.environ.get("REDIS_PROTOCOL", "redis")
CELERY_BROKER_URL = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"
CELERY_RESULT_BACKEND = \
    REDIS_PROTOCOL + "://" + REDIS_HOST + ":" + REDIS_PORT + "/0"
