# Проектная работа 10 спринта

Командная работа https://github.com/AnnaKPolyakova/notifications_sprint_1  
Над проектом работали:  https://github.com/AnnaKPolyakova/ (Анна Полякова)

## Описание работы проекта:
[Схема бд](schemas%2Fnotification_models_schema.plantuml)  
[Схема работы проекта](schemas%2Fschema.plantuml)

#### Создание уведомлений:
Создать разовые уведомление можно:
- через API (документация тут http://127.0.0.1:8004/api/schema/redoc/). 
  Необходимо создать Notification и привязать к нему UsersNotification с 
  указанием id пользователей (кому направить уведомление). Если уведомление 
  должно быть срочным, то необходимо указать is_express. Срочные 
  уведомления попадают в отдельную очередь с более высоким приоритетом
- админ панель (http://127.0.0.1:8004/admin/)

Так же можно сформировать регулярное уведомление (NotificationFrequency)
Необходимо указать: id пользователей в виде списка, ссылка на Notification и 
периодичность.
После перезагрузки celery - новая таска будет запускаться по расписанию

После создания NotificationFrequency информация о нем попадает в очередь, 
консьюмер достает их оттуда и отправляет сообщения.

В случае, если что-то пойдет не так и при создании UsersNotification 
информация о нем не попадет в очередь для обработки, то поле такого объекта 
is_sent_to_queue будет помечено, как False. Специальная регулярная таска 
будет отыскивать такие сообщение и пробовать поставить их в очередь снова и 
снова.

Кол-во коньсюмеров для запуска и их минимальное и максимальное кол-во 
указывается в env. Перед запуском происходит проверка, уже имеющегося кол-ва 
консьюмеров и вычисляется какое ко-во можно запустить.

Если кол-во сообщений формируемых за раз больше 100, то последующшие 
сообщения отправляются в очередь с задержкой


#### Запуск проекта в контейнерах docker

* `docker-compose up -d --build`
* `docker-compose exec producer python notification_producer/manage.py createsuperuser`

Для остановки контейнера:

* `docker-compose down --rmi all --volumes`


#### Запуск проекта частично в контейнерах docker

* `docker-compose -f docker-compose-local.yml up --build`
* `cd notification_producer/`
* `celery -A schedule.celery_app worker -l info`
* `celery -A schedule.celery_app beat -l info`

Для остановки контейнера:

* `docker-compose -f docker-compose-local.yml down --rmi all --volumes`


Для создания админа:
* `python notification_producer/manage.py createsuperuser`
