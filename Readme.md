## Тестовое задание для idalite:

Реализованно всё, кроме аутентификации - поздно заметил изменение в ТЗ. Думаю, что в ближайшее время добавлю.


### Комментарий:
* `make`  
  Для сокращения команд использовал `make`.  Изначально хотел написать более функциональный `Makefile` для конфигурации проекта. Однако, похоже, `make` оказался не лучшим выбором. Собираюсь переписать на `poetry` (исправлю описание когда сделаю).
  
  Все команды буду приводить через `make` и без.

* `API`  
  - входная точка `/managers/{user_id}` используется для получения списка менеджеров, которых видет `user` с id `user_id` используется входная точка `/managers/{user_id}`.
  - входная точка `/managers/list` используется для получения полного списка менеждеров

### Запуск в `docker-compose`

Cборка и запуск `docker-compose`:

```console
$ make docker-build-test 
$ make docker-up-test

# alternative
$ docker-compose --env-file config/envs/compose.test.env build
$ docker-compose --env-file config/envs/compose.test.env run
```
Тестирование запущенного `docker-compose`:

```console
$ make run-test-docker

# alternative
$ ENV=config/envs/compose.test.env python -m pytest tests/docker
```

### Запуск локально
Используются  `.env` файлы `config/envs/default.env` и `config/envs/test.env` для тестов.

Установка библиотек и инициализация базы данных:
```console
$ make install install-dev alembic-upgrade seed-database

# alternative
$ pip install -r requirements.txt -r requirements_dev.txt
$ alembic upgrade head
$ python -m tests.seed_database

```

Запуск сервера:
```console
$ make run-gunicorn

# alternative:  
$ gunicorn app.main:app -k uvicorn.workers.UvicornWorker -c config/gunicorn_conf.py
```

Запуск тестов:
```console
$ make run-tests-unit
$ make run-tests-integration

# alternative:
$ ENV=config/envs/test.env python -m pytest tests/unit
$ ENV=config/envs/test.env pytest -m pytest tests/integration
```
