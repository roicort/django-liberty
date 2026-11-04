#!/bin/sh
set -eu

DISABLE_MIGRATIONS="${DISABLE_MIGRATIONS:-false}"

if [ "$DISABLE_MIGRATIONS" != "true" ] && [ "$DISABLE_MIGRATIONS" != "True" ]; then
    echo "Applying database migrations..."
    uv run --no-sync manage.py migrate --noinput

    set +e
    uv run --no-sync manage.py superuser_exists
    superuser_status=$?
    set -e

    if [ "$superuser_status" -eq 10 ]; then
        echo "Configured superuser not found; running first-time configuration..."
        sh ./first_run.sh
    elif [ "$superuser_status" -ne 0 ]; then
        exit "$superuser_status"
    fi
fi

exec "$@"
