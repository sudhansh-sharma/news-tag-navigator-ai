#!/bin/sh
set -e

# Run database migrations
python manage.py makemigrations --noinput

# Run database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3 