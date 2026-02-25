WITH latest_import AS (

    SELECT *
    FROM {{ ref('stg_fpl__latest_import') }}
    WHERE endpoint = 'bootstrap-static/'

),

scoring AS (

SELECT
    li.imported_at,
    li.id AS import_id,
    endpoint AS api_endpoint,
    s.*
FROM latest_import li,
LATERAL jsonb_to_record(li.raw_json->'game_config'->'scoring') AS s(
    bps int,
    bonus int,
    saves int,
    starts int,
    threat int,
    assists int,
    mng_win jsonb,
    tackles int,
    mng_draw jsonb,
    mng_loss int,
    ict_index int,
    influence int,
    long_play int,
    own_goals int,
    red_cards int,
    creativity int,
    recoveries int,
    short_play int,
    clean_sheets jsonb,
    goals_scored jsonb,
    yellow_cards int,
    expected_goals int,
    goals_conceded jsonb,
    penalties_saved int,
    expected_assists int,
    mng_clean_sheets jsonb,
    mng_goals_scored jsonb,
    mng_underdog_win jsonb,
    penalties_missed int,
    mng_underdog_draw jsonb,
    special_multiplier int,
    defensive_contribution jsonb,
    expected_goals_conceded int,
    expected_goal_involvements int,
    clearances_blocks_interceptions int
    )
)

select * from scoring