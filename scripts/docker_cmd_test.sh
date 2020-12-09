#!/bin/sh
gunicorn app.main:app -k uvicorn.workers.UvicornWorker -c config/gunicorn_conf.py