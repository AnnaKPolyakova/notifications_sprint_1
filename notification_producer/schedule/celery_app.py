import logging
import os
import time

import django
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("notifications")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(['schedule'])

django.setup()

logger = logging.getLogger(__name__)


def get_regular_tasks():
    tasks = {}
    from admin_panel.models import NotificationFrequency
    notifications = NotificationFrequency.objects.all()
    for notification in notifications:
        try:
            tasks.update(
                {
                    'run_regular_task_sent_express_notifications_{slug}'.
                    format(slug=notification.slug): {
                        "task": 'schedule.tasks.send_notifications',
                        "schedule": 10,
                        "args": [notification.slug],
                    },
                }
            )
        except Exception as error:
            logger.error(error)
    return tasks


def get_all_tasks():
    tasks = {
        'run_save_missing_users_notifications_to_rabbitmq_task': {
            "task":
                'schedule.tasks.save_missing_users_notifications_to_rabbitmq',
            "schedule": 10,
        },
    }
    tasks.update(get_regular_tasks())
    time.sleep(20)
    return tasks


app.conf.beat_schedule = get_all_tasks()
