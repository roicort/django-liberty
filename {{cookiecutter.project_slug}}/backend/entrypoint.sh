#!/bin/sh
set -e

IS_CELERY="${IS_CELERY:-false}"

if [ "$IS_CELERY" = "true" ]; then
    echo "Celery container detected, skipping database setup and app bootstrap..."
    exec "$@"
fi

# Check if the initialization has already been done and that we enabled automatic migration
if [ "${DISABLE_DB_MIGRATIONS}" != "true" ] && [ ! -f ./db_status ]; then
    echo "Running database setup and migrations..."

    uv run --no-sync manage.py makemigrations
    uv run --no-sync manage.py migrate

    # Mark initialization as done
    echo "Successfuly migrated DB!"
    touch ./db_status
fi

if [ ! -f ./first_config ]; then
    echo "Running first configuration..."

    uv run --no-sync manage.py ensure_oidc_client
    uv run --no-sync manage.py ensure_superuser
    uv run --no-sync manage.py collectstatic --noinput

    # Mark first configuration as done
    echo "Successfuly configured the app!"
    touch ./first_config
fi


# Continue with the original Docker command
exec "$@"
