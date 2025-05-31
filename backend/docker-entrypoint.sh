#!/bin/bash
set -e

export PYTHONUNBUFFERED=1
export PYTHONIOENCODING=UTF-8

export PYTHONSTARTUP="/app/suppress_logs.py"

echo "Starting Django application..."

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if credentials provided
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "Creating superuser..."
  python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="$DJANGO_SUPERUSER_USERNAME").exists():
    User.objects.create_superuser("$DJANGO_SUPERUSER_USERNAME", "$DJANGO_SUPERUSER_EMAIL", "$DJANGO_SUPERUSER_PASSWORD")
END
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120