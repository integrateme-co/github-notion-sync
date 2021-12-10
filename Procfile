release: python manage.py makemigrations
release: python manage.py migrate

web: python manage.py migrate && gunicorn config.wsgi
