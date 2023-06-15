import os

from config.settings import BASE_DIR

STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

if int(os.environ.get('LOCAL_SETTINGS', 1)) == 1:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'notification_producer/static/'),
    )
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "notification_producer/static")
