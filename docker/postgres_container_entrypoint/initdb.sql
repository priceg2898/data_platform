-- Create user if not exists (safe pattern)
DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = 'analytics_user'
   ) THEN
      CREATE ROLE analytics_user LOGIN PASSWORD 'pw';
   END IF;
END
$$;

-- Create database only if it doesn't exist
SELECT 'CREATE DATABASE analytics OWNER analytics_user'
WHERE NOT EXISTS (
    SELECT FROM pg_database WHERE datname = 'analytics'
)\gexec

\c analytics

CREATE TABLE IF NOT EXISTS public.bronze__raw_landing (
    id SERIAL PRIMARY KEY,
    base_url TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    raw_json JSONB,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);