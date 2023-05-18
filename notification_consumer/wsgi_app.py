from gevent import monkey

monkey.patch_all()

from notification_consumer.notification_app import create_notification_app

app = create_notification_app()
