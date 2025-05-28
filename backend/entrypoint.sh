#!/bin/sh
set -e

# Run database migrations
python manage.py makemigrations --noinput

# Run database migrations
python manage.py migrate --noinput

# Create superuser if it doesn't exist
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
END
fi

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3 