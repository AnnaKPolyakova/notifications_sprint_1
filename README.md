# Проектная работа 10 спринта

Проектные работы в этом модуле в команде. Задания на спринт вы найдёте внутри тем.

#### Запуск проекта в контейнерах docker

* `docker-compose up -d --build`

Для остановки контейнера:

* `docker-compose down --rmi all --volumes`


#### Запуск проекта частично в контейнерах docker

* `docker-compose -f docker-compose-local.yml up --build`

Для остановки контейнера:

* `docker-compose -f docker-compose-local.yml down --rmi all --volumes`