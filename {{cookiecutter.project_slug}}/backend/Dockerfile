FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    git \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml ./

RUN poetry new venv && poetry run pip install GDAL==$(gdal-config --version) && poetry install

COPY src .

RUN poetry run python manage.py collectstatic --noinput

ENTRYPOINT ["bash","entrypoint.sh"]
CMD ["poetry", "run", "gunicorn","--bind", ":8000", "main.wsgi:application"]
