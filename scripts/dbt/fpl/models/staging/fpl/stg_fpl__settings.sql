WITH latest_import AS (

    SELECT *
    FROM {{ ref('stg_fpl__latest_import') }}
    WHERE endpoint = 'bootstrap-static/'

),

settings AS (

    SELECT
        imported_at,
        latest_import.id AS import_id,
        endpoint AS api_endpoint,
        st.*
    FROM latest_import,
    LATERAL jsonb_to_record(latest_import.raw_json->'game_config'->'settings') AS st(
        timezone text,
        entry_per_event boolean
    )

)

SELECT * FROM settings