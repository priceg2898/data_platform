SELECT
    rl.imported_at,
    rl.id AS import_id,
    endpoint AS api_endpoint,
    p.*
FROM public.bronze__raw_landing rl,
LATERAL jsonb_to_recordset(raw_json->'phases') AS p(
    id int,
    name text,
    stop_event int,
    start_event int,
    highest_score int
)
WHERE endpoint = 'bootstrap-static/'