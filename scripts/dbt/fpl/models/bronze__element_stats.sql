SELECT
    rl.imported_at,
    rl.id AS import_id,
    endpoint AS api_endpoint,
    es.*
FROM public.bronze__raw_landing rl,
LATERAL jsonb_to_recordset(raw_json->'element_stats') AS es(
    name  text,
    label text
)
WHERE endpoint = 'bootstrap-static/'