FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /work_dir

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    ca-certificates \
    apt-transport-https \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install poetry \
    && pip install poetry-plugin-export

COPY docker/container__scripts/pyproject.toml docker/container__scripts/poetry.lock /work_dir/
COPY dags /opt/airflow/dags
COPY scripts /work_dir/scripts

RUN poetry export -f requirements.txt \
    --output requirements.txt \
    --without-hashes \
    && pip install --no-cache-dir -r requirements.txt
