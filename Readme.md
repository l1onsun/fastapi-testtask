### Тестовое задаеие для idalite:

Реализованно всё кроме ауентификации - поздно заметил изменение в ТЗ. Думаю, что в ближайшее время добавлю.


#### Комментарий:
Для сокращения команд использовал `make`.  Изначально хотел написать широко-функциональный `Makefile` для конфигурации проекта. Однако, похоже, `make` оказался не лучшим выбором. Если успею перепишу на `poetry`  

Все каманды буду приводить через `make` и без.


### Запуск в `docker-compose`

Команды, чтобы собрать и запустить `docker-compose` (`make` используется только для сокращения длинных команд. Изначально хотел написать широко-функциональный `Makefile` для конфигурации проекта. Но `make` оказался не лучшим выбором. Если успею перепишу на `poetry` ):

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
PYTHONPATH=. ENV=config/envs/compose.test.env pytest tests/docker
```

### Запуск локально
Используются  `.env` файлы `config/envs/default.env` и `config/envs/test.env` для тестов.

Установка библиотек:


```console
$ make install install-dev

# alternative
$ pip install -r requirements.txt -r requirements_dev.txt

```

Запуск сервера:
```console
$ make run-guvncorn

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