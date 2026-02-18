SELECT
    rl.imported_at,
    rl.id AS import_id,
    endpoint AS api_endpoint,
    c.*
FROM public.bronze__raw_landing rl,
LATERAL jsonb_to_recordset(raw_json->'chips') AS c(
    id          int,
    name        text,
    number      int,
    chip_type   text,
    overrides   jsonb,
    stop_event  int,
    start_event int
)
WHERE endpoint = 'bootstrap-static/'
