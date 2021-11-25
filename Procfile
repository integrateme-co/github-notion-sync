release: python manage.py makemigration
release: python manage.py migrate

web: python manage.py migrate && gunicorn config.wsgi
