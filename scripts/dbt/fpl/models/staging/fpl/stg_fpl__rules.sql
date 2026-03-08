WITH latest_import AS (

    SELECT *
    FROM {{ ref('stg_fpl__latest_import') }}
    WHERE endpoint = 'bootstrap-static/'

),

rules AS (

SELECT
    li.imported_at,
    li.id AS import_id,
    endpoint AS api_endpoint,
    r.*
FROM latest_import li,
LATERAL jsonb_to_record(li.raw_json->'game_config'->'rules') AS r(
    cup_type int,
    transfers_cap int,
    squad_squadplay int,
    squad_squadsize int,
    stats_form_days int,
    featured_entries jsonb,
    percentile_ranks jsonb,
    squad_team_limit int,
    cup_stop_event_id int,
    squad_special_max int,
    squad_special_min int,
    squad_total_spend int,
    cup_start_event_id int,
    league_prefix_public text,
    cup_qualifying_method text,
    league_points_h2h_win int,
    transfers_sell_on_fee numeric,
    ui_use_special_shirts boolean,
    underdog_differential int,
    league_join_public_max int,
    league_points_h2h_draw int,
    league_points_h2h_lose int,
    ui_currency_multiplier int,
    league_join_private_max int,
    max_extra_free_transfers int,
    sys_vice_captain_enabled boolean,
    league_h2h_tiebreak_stats jsonb,
    league_max_size_public_h2h int,
    league_max_size_private_h2h int,
    ui_special_shirt_exclusions jsonb,
    element_sell_at_purchase_price boolean,
    league_max_size_public_classic int,
    league_max_ko_rounds_private_h2h int,
    league_ko_first_instead_of_random boolean
    )
)

select * from rules