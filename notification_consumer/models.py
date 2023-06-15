from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base

from notification_consumer.db import engine

# with DatabaseManager
metadata = MetaData()
metadata.reflect(bind=engine)
Base = automap_base(metadata=metadata)
Base.prepare()

Users = Base.classes.auth_user
Notification = Base.classes.admin_panel_notification
UsersNotification = Base.classes.admin_panel_usersnotification
UsersUnsubscribe = Base.classes.admin_panel_usersunsubscribe
