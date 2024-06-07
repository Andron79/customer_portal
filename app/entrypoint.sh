#!/bin/sh
set -e
echo "Start Migrations "
python manage.py migrate
python manage.py collectstatic --noinput


exec "$@"
