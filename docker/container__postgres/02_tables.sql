CREATE TABLE IF NOT EXISTS public.bronze__raw_landing (
    id SERIAL PRIMARY KEY,
    base_url TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    raw_json JSONB,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

