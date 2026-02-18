SELECT
    rl.imported_at,
    rl.id AS import_id,
    endpoint AS api_endpoint,
    st.*
FROM public.bronze__raw_landing rl,
LATERAL jsonb_to_record(rl.raw_json->'game_config'->'settings') AS st(
    timezone text,
    entry_per_event boolean
)
WHERE endpoint = 'bootstrap-static/'