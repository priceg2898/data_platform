SELECT
    imported_at,
    rl.id AS import_id,
    endpoint AS api_endpoint,
    e.*
FROM public.bronze__raw_landing rl,
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
WHERE endpoint = 'bootstrap-static/'