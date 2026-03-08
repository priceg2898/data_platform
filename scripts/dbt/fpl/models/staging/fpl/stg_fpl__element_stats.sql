WITH latest_import AS (

    SELECT *
    FROM {{ ref('stg_fpl__latest_import') }}
    WHERE endpoint = 'bootstrap-static/'

),

event_stats AS (

SELECT
    li.imported_at,
    li.id AS import_id,
    endpoint AS api_endpoint,
    es.*
FROM latest_import li,
LATERAL jsonb_to_recordset(raw_json->'element_stats') AS es(
    name  text,
    label text
)

)

SELECT * fROM event_stats