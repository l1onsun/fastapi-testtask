#!/bin/sh
python -m scripts.switch_environment docker development
python -m scripts.manage_database migrate seed-test
gunicorn app.main:app -k uvicorn.workers.UvicornWorker -c config/gunicorn_conf.py