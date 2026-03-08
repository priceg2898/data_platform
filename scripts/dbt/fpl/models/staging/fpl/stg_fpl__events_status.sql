WITH latest_import AS (

    SELECT *
    FROM {{ ref('stg_fpl__latest_import') }}
    WHERE endpoint = 'event-status/'

),

event_status AS (

SELECT
    li.imported_at,
    li.id AS import_id,
    endpoint AS api_endpoint,
    s.*
FROM latest_import li,
LATERAL jsonb_array_elements(raw_json->'status') AS s_item,
LATERAL jsonb_to_record(s_item.value) AS s(
    date date,
    event int,
    points text,
    bonus_added boolean)
)

SELECT * FROM event_status