## Тестовое задание для idalite:

Реализованно всё, кроме аутентификации - поздно заметил изменение в ТЗ. Постараюсь успеть добавить до проверки.


### Комментарий:
* `make`  
  Для сокращения команд использовал `make`.  Изначально пробовал написать более функциональный `Makefile` для конфигурации проекта. Однако, похоже, `make` оказался не лучшим выбором (неудобно пробрасывать параметры скриптам). Собираюсь переписать на `poetry`. Когда сделаю, исправлю описание.
  
  Все команды буду приводить через `make` и без.

* `API`  
  - входная точка `/managers/{user_id}` используется для получения списка менеджеров, которых видет пользователь с `user_id`
  - входная точка `/managers/list` используется для получения полного списка менеджеров
 
* `env-files`  
  Для конфигурации проекта использовал `.env` файлы. Они расположены в `config/envs/`:
  - `default.env` - используется по умолчанию
  - `test.env` - окружение для тестирования локально
  - `compose.default.env` - окружение для `docker-compose` контейнеров по умолчанию
  - `compose.test.env` - окружение для тестирования `docker-compose` контейнеров
  Для запуска `python`-скрипта с нужным окружением: `ENV=path/to/.env python some_script.py`
  
  (Конечено `.env` файлы не должны быть добавлены в репозиторий, так как потенциально содержат секретную информацию. Но так как проект тестовый, я решил их добавить)

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
