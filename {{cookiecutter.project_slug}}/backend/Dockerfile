FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1

RUN apk update && apk add --no-cache \
    build-base \
    git \
    gdal-dev \
    geos-dev \
    proj-dev

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml ./

RUN poetry install

COPY src .

RUN poetry run python manage.py collectstatic --noinput

ENTRYPOINT ["sh","entrypoint.sh"]
CMD ["poetry", "run", "gunicorn","--bind", ":8000", "main.wsgi:application"]