from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from notification_consumer.settings import notification_consumer_settings

engine = create_engine(
    'postgresql://{username}:{password}@{host}/{db_name}'.format(
        username=notification_consumer_settings.postgres_user,
        password=notification_consumer_settings.postgres_password,
        host=notification_consumer_settings.postgres_host,
        db_name=notification_consumer_settings.postgres_db
    )
)


class DatabaseManager:
    def __init__(self, engine_obj):
        self.engine = engine_obj
        self.session = None

    def __enter__(self):
        self.session = sessionmaker(bind=self.engine)()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()
