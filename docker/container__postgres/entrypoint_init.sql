CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE IF NOT EXISTS public.bronze__raw_landing (
    id SERIAL PRIMARY KEY,
    base_url TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    raw_json JSONB,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE USER airflow_user WITH PASSWORD 'airflow';
CREATE DATABASE airflow OWNER airflow_user;
