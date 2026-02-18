SELECT
    rl.imported_at,
    rl.id AS import_id,
    endpoint AS api_endpoint,
    s.*
FROM bronze__raw_landing rl,
LATERAL jsonb_array_elements(raw_json->'status') AS s_item,
LATERAL jsonb_to_record(s_item) AS s(
    date date,
    event int,
    points text,
    bonus_added boolean
)
WHERE rl.endpoint = 'event-status/'
