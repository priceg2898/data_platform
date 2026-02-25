WITH latest_import AS (

    SELECT *
    FROM {{ ref('stg_fpl__latest_import') }}
    WHERE endpoint = 'bootstrap-static/'

),

phases AS (

SELECT
    li.imported_at,
    li.id AS import_id,
    endpoint AS api_endpoint,
    p.*
FROM latest_import li,
LATERAL jsonb_to_recordset(raw_json->'phases') AS p(
    id int,
    name text,
    stop_event int,
    start_event int,
    highest_score int
    )
)

select * from phases