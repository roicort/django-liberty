#!/bin/sh
set -eu

uv run --no-sync manage.py ensure_oidc_client
uv run --no-sync manage.py ensure_superuser
# uv run --no-sync manage.py loaddata makes model_generations base_models
