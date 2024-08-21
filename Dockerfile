FROM python:3.12-slim

RUN pip install --upgrade pip && pip install poetry

ENV POETRY_VERSION=1.8.2

WORKDIR /code

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create true && poetry install --no-root --no-interaction

COPY . .