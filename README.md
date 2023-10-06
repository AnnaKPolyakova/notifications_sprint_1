# Project work 10 sprint
 
## Description of the project:
[DB schema](schemas%2Fnotification_models_schema.plantuml)
[Project work scheme](schemas%2Fschema.plantuml)

#### Creating notifications:
You can create one-time notifications:
- via API (documentation here http://127.0.0.1:8004/api/schema/redoc/).
   You need to create a Notification and bind UsersNotification to it with
   indicating the user id (to whom the notification should be sent). If notice
   must be urgent, then is_express must be specified. Urgent
   notifications go into a separate queue with a higher priority.

   To create a notification to the administrator, you can use authorization
   via login password or jwt token.
  
   To create a notification through a third-party application, the administrator must
   register it through the admin panel and give it a login and password,
   which must be specified in headers in the 'Authorization' format: 'login password'

- admin panel (http://127.0.0.1:8004/admin/)

#### Formation of a request by the user via the API:
   Since a third-party server is responsible for user authorization,
   you need to add a token in the 'Authorization' format to the request headers: 'token'


You can also generate a regular notification (NotificationFrequency)
You must specify: user ids in the form of a list, a link to Notification and
periodicity.
After rebooting celery, the new task will be launched according to schedule

After creating a NotificationFrequency, information about it goes into the queue,
the consumer takes them out and sends messages.

In case something goes wrong while creating UsersNotification
information about it will not be queued for processing, then the field of such an object
is_sent_to_queue will be marked as False. Special regular task
will look for such messages and try to queue them again and
again.

Number of consumers to launch and their minimum and maximum number
specified in env. Before starting, a check is made to check the existing quantity
consumers and calculates how many can be launched.

If the number of messages generated at a time is more than 100, then subsequent
messages are sent to the queue with a delay


#### Running a project in docker containers

* `docker-compose up -d --build`
* `docker-compose exec producer python notification_producer/manage.py createsuperuser`

To stop the container:

* `docker-compose down --rmi all --volumes`


#### Running the project partially in docker containers

* `docker-compose -f docker-compose-local.yml up --build`
* `cd notification_producer/`
* `celery -A schedule.celery_app worker -l info`
* `celery -A schedule.celery_app beat -l info`

To stop the container:

* `docker-compose -f docker-compose-local.yml down --rmi all --volumes`


To create an admin:
* `python notification_producer/manage.py createsuperuser`
