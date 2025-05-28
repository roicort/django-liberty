#!/bin/sh
set -e

# Check if the initialization has already been done and that we enabled automatic migration
if [ "${DISABLE_DB_MIGRATIONS}" != "true" ] && [ ! -f /app/db_status ]; then
    echo "Running database setup and migrations..."

    uv run manage.py makemigrations
    uv run manage.py migrate

    # Mark initialization as done
    echo "Successfuly migrated DB!"
    touch /app/db_status
fi

if [ ! -f /app/first_config ]; then
    echo "Running first configuration..."

    uv run manage.py creatersakey
    uv run manage.py import_oidc_config
    uv run manage.py createsuperuser --noinput --first_name admin --last_name admin
    uv run manage.py collectstatic --noinput

    # Mark first configuration as done
    echo "Successfuly configured the app!"
    touch /app/first_config
fi


# Continue with the original Docker command
exec "$@"
