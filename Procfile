release: python manage.py makemigrations
release: python manage.py migrate

web: python manage.py migrate && DJANGO_SUPERUSER_PASSWORD=admin ./manage.py createsuperuser --no-input --username=admin --email=admin@integrateme.co && gunicorn config.wsgi
