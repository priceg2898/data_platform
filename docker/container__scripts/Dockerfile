FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /work_dir

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install poetry \
    && pip install poetry-plugin-export \
    && pip install dbt-core dbt-postgres

COPY docker/container__scripts/pyproject.toml docker/container__scripts/poetry.lock /work_dir

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN pip install --no-cache-dir -r requirements.txt

#COPY scripts/fpl_api_extract_and_load.py /app

CMD ["tail", "-f", "/dev/null"]


