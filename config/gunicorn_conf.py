from config.gunicorn_env import gunicorn_env
import multiprocessing


def count_workers():
    if gunicorn_env.web_concurrency:
        workers = gunicorn_env.web_concurrency
    else:
        cores = multiprocessing.cpu_count()
        default_web_concurrency = gunicorn_env.workers_per_core * cores
        workers = max(int(default_web_concurrency), gunicorn_env.max_workers)

    assert workers > 0
    return workers


# Gunicorn config
bind = f"{gunicorn_env.host}:{gunicorn_env.port}"
workers = count_workers()
timeout = gunicorn_env.timeout
keepalive = gunicorn_env.keepalive
