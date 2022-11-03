#!/bin/sh
if [ 1 ]
then
    echo "Waiting for postgres..."
    while ! nc -z postgres $POSTGRES_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi
  python manage.py flush --no-input
  python manage.py collectstatic --noinput &&
  python manage.py makemigrations &&
  python manage.py migrate &&
  python manage.py createsuperuser --noinput
  python manage.py init_test_users
  python manage.py runserver 0.0.0.0:8000
exec "$@"