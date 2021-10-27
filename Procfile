release: python manage.py makemigration
release: python manage.py migrate

web: gunicorn config.wsgi:application --log-file=-