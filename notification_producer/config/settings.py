import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

include(
    "components/database.py",
    "components/application_definition.py",
    "components/password_validators.py",
    "components/internationalization.py",
    "components/static_files.py",
    "components/rabbitmq.py",
    "components/logging.py",
    "components/other.py",
    "components/rest_framework.py",
    "components/celery.py",
)

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = int(os.environ.get("DEBUG", 0)) == 1

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", '').split(' ')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


if DEBUG:
    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]
