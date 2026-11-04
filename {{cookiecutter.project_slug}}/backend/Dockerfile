FROM python:3.14.4-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONPATH=/app/src

RUN apk add --no-cache \
    build-base \
    git \
    gdal-dev \
    geos-dev \
    openssl \
    proj-dev

WORKDIR /app

COPY pyproject.toml uv.lock ./

#RUN --mount=type=cache,target=/root/.cache/uv \
RUN uv sync --locked --no-dev --no-install-project

COPY . .

#RUN --mount=type=cache,target=/root/.cache/uv \
RUN uv sync --locked --no-dev

RUN uv run --no-sync manage.py collectstatic --noinput

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
CMD ["sh", "-c", "exec uv run --no-sync gunicorn --bind 0.0.0.0:${PORT:-8000} main.wsgi:application --workers ${GUNICORN_WORKERS:-4} --timeout 0"]
