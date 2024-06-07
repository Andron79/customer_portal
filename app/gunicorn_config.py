import os


bind = "0.0.0.0:8000"
worker_class = "gevent"
workers = int(_) if (_ := os.getenv("APP_GUNICORN_WORKERS")) else 4
timeout = int(_) if (_ := os.getenv("APP_GUNICORN_TIMEOUT")) else 600
