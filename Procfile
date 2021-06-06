worker: cd backend/ && celery -A config worker -l info
scheduler: cd backend/ && celery -A config beat -l info
web: cd backend/ && gunicorn backend.config.wsgi:application --log-file -
