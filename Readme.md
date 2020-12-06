## Тестовое задание:

по ТЗ: https://www.notion.so/ad50f98119424a7d9fd88f69a07f4a47


### Комментарий:
* `make`  
  Для сокращения команд использовал `make`.  Изначально собирался написать более функциональный `Makefile` для конфигурации проекта. Однако, похоже, `make` оказался не лучшим выбором (неудобно пробрасывать параметры скриптам). Перепишу на `python` скрипты когда дойдут руки
  
  Все команды буду приводить через `make` и без.

* `API`
  - входная точка `/managers/{user_id}` используется для получения списка менеджеров, которых видет пользователь с `user_id` (см. ТЗ)
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
# install test dependensies
$ make install-test
# run tests
$ make run-test-docker

# alternative
$ pip install -r requirements.txt
$ ENV=config/envs/compose.test.env python -m pytest tests/docker
```

### Запуск локально
Используются  `.env` файлы `config/envs/default.env` и `config/envs/test.env` для тестов.

Установка библиотек и инициализация базы данных:
```console
$ make install install-test
$ make alembic-upgrade seed-database

# alternative
$ pip install -r requirements.txt -r requirements_test.txt
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
