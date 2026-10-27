#!/bin/sh

echo "Running database migrations..."
python manage.py migrate

echo "Starting application..."
exec "$@"