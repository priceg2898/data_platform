FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install poetry \
    && pip install poetry-plugin-export

COPY /pyproject.toml /poetry.lock /app/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN pip install --no-cache-dir -r requirements.txt

COPY ingestion/etl/__main__.py /app

CMD ["tail", "-f", "/dev/null"]


