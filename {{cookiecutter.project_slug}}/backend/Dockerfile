FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1

RUN apk update && apk add --no-cache \
    build-base \
    git \
    gdal-dev \
    geos-dev \
    proj-dev

WORKDIR /app

COPY pyproject.toml ./

COPY src .

RUN uv run manage.py collectstatic --noinput

ENTRYPOINT ["sh","entrypoint.sh"]
CMD ["uv", "run", "gunicorn","--bind", ":8000", "main.wsgi:application"]