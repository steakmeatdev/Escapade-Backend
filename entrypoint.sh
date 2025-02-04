#!/bin/sh

if [ "$SQL_ENGINE" = "django.db.backends.postgresql" ] 
then
    echo "Check if database is running..."

    # Checking if the database is reachble at the given host and port (in .env.dev).
    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "The database is up and running"
fi

python manage.py makemigrations
python manage.py migrate

# exec to run whatever I want
exec "$@"