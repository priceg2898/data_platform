WITH latest_import AS (

    SELECT *
    FROM {{ ref('stg_fpl__latest_import') }}
    WHERE endpoint = 'bootstrap-static/'

),

teams AS (

    SELECT
        imported_at,
        latest_import.id AS import_id,
        endpoint AS api_endpoint,
        t.*
    FROM latest_import,
    LATERAL jsonb_to_recordset(raw_json->'teams') AS t(
        id int,
        code int,
        pulse_id int,
        name text,
        short_name text,
        team_division int,
        played int,
        win int,
        draw int,
        loss int,
        points int,
        position int,
        form text,
        strength int,
        strength_attack_home int,
        strength_attack_away int,
        strength_defence_home int,
        strength_defence_away int,
        strength_overall_home int,
        strength_overall_away int,
        unavailable boolean
    )

)

SELECT * FROM teams