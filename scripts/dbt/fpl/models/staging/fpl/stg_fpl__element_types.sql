WITH latest_import AS (
    SELECT *
    FROM {{ ref('stg_fpl__latest_import') }}
    WHERE endpoint = 'bootstrap-static/'
),

element_types AS
(
SELECT
    imported_at,
    li.id AS import_id,
    endpoint AS api_endpoint,
    e.*
FROM latest_import li,
LATERAL jsonb_to_recordset(raw_json->'element_types') AS e(
    id                      int,
    plural_name             text,
    squad_select            int,
    element_count           int,
    singular_name           text,
    squad_max_play          int,
    squad_min_play          int,
    squad_max_select        int,
    squad_min_select        int,
    plural_name_short       text,
    ui_shirt_specific       boolean,
    singular_name_short     text,
    sub_positions_locked    jsonb
)

)

select * from element_types
