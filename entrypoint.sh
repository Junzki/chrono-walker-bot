#!/bin/sh

python manage.py migrate

export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@example.com
export DJANGO_SUPERUSER_PASSWORD=change-me-admin-password
python manage.py createsuperuser --no-input


uwsgi --ini uwsgi.ini
