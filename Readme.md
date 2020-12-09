## Тестовое задание:

по ТЗ: https://www.notion.so/ad50f98119424a7d9fd88f69a07f4a47


### Комментарий:
* `pipenv`  
  Перешел на [pipenv][https://github.com/pypa/pipenv] для управления зависимостями и упрощения работы с окружением.

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
  
### Установка зависимостей:
Если отсутсвует `pipenv`:
```console
$ pip install pipenv
```
Установка необходимых зависимостей:
```console
$ pipenv sync --dev
```

### Запуск в `docker-compose`
Установка нужного окружения  (создаст `symlink` `.env`)
```console
$ pipenv run switch development docker
```

Cборка и запуск `docker-compose`:

```console
$ docker-compose build
$ docker-compose run
```
Тестирование запущенного `docker-compose`:

```console
$ pipenv run pytest
```

### Запуск локально
Окружение (необходимо отредактировать `config/envs/.env.development`):
```console
$ pipenv run switch development local
```
Инициализация базы данных и заполнения тестовыми данными:
```console
$ pipenv run database migrate seed-test
```

Запуск сервера:
```console
$ pipenv run gunicorn
```

Запуск тестов:
```console
$ pipenv run pytest
```
