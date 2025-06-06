FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl
RUN pip install --no-cache-dir poetry

COPY app ./app/
COPY .env ./app/
COPY pyproject.toml poetry.lock* ./app/

WORKDIR app
RUN poetry self add poetry-plugin-shell \
    && poetry install