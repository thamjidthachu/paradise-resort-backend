#!/bin/sh

# Exit on error
set -e

# Run migrations
python manage.py migrate --noinput

# Collect static files (optional, if you use static)
# python manage.py collectstatic --noinput

# Start server
python manage.py runserver 0.0.0.0:8000
