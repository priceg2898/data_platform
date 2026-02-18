FROM postgres:15

# Set environment variables (optional, can also be set in docker-compose)
ENV POSTGRES_USER=local_testing
ENV POSTGRES_PASSWORD=local_testing_password
ENV POSTGRES_DB=database

COPY docker/container__postgres/01_schemas.sql docker/container__postgres/02_tables.sql /docker-entrypoint-initdb.d/
