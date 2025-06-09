web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn ecommerce_api.wsgi:application --bind 0.0.0.0:$PORT --log-file -
worker: celery -A ecommerce_api worker --loglevel=info
beat: celery -A ecommerce_api beat --loglevel=info --pidfile=/tmp/celerybeat.pid
