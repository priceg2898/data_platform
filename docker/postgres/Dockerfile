FROM postgres:15

# Set environment variables (optional, can also be set in docker-compose)
ENV POSTGRES_USER=local_testing
ENV POSTGRES_PASSWORD=local_testing_password
ENV POSTGRES_DB=test_db

# Copy SQL scripts into docker-entrypoint-initdb.d
# Scripts here run automatically on first container startup
COPY 01_schemas.sql 02_tables.sql 03_views.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
