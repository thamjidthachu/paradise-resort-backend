#!/bin/sh

# Exit on error
set -e

echo "Waiting for PostgreSQL..."

# Function to test PostgreSQL connection
postgres_ready() {
  python << END
import sys
import psycopg2
import os
from decouple import config

try:
    psycopg2.connect(
        dbname=config('DB_NAME'),
        user=config('DB_USER'),
        password=config('DB_PASSWORD'),
        host=config('DB_HOST'),
        port=config('DB_PORT', default=5432)
    )
except psycopg2.OperationalError:
    sys.exit(1)
sys.exit(0)
END
}

# Wait for PostgreSQL to be ready
until postgres_ready; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up - executing command"

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start server
python manage.py runserver 0.0.0.0:8000
