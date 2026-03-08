WITH latest_import AS (

    SELECT *
    FROM {{ ref('stg_fpl__latest_import') }}
    WHERE endpoint = 'bootstrap-static/'

),

chips AS (

SELECT
    li.imported_at,
    li.id AS import_id,
    endpoint AS api_endpoint,
    c.*
FROM latest_import li,
LATERAL jsonb_to_recordset(raw_json->'chips') AS c(
    id          int,
    name        text,
    number      int,
    chip_type   text,
    overrides   jsonb,
    stop_event  int,
    start_event int
)

)

SELECT * FROM chips