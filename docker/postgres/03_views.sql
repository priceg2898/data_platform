CREATE OR REPLACE VIEW bronze.v_teams AS (
SELECT imported_at, rl.id AS import_id, endpoint as api_endpoint, t.*
FROM bronze.raw_landing rl,
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
));

CREATE OR REPLACE VIEW bronze.v_events AS (
SELECT imported_at, rl.id AS import_id, endpoint as api_endpoint, e.*
 FROM bronze.raw_landing rl,
 LATERAL jsonb_to_recordset(raw_json->'events') AS e(
     id                          int,
     name                        text,
     is_next                     boolean,
     finished                    boolean,
     released                    boolean,
     can_enter                   boolean,
     can_manage                  boolean,
     is_current                  boolean,
     is_previous                 boolean,
     top_element                 int,
     data_checked                boolean,
     ranked_count                bigint,
     release_time                timestamptz,
     deadline_time               timestamptz,
     highest_score               int,
     most_selected               int,
     most_captained              int,
     transfers_made              int,
     average_entry_score         int,
     cup_leagues_created         boolean,
     deadline_time_epoch         bigint,
     most_transferred_in         int,
     most_vice_captained         int,
     highest_scoring_entry       bigint,
     h2h_ko_matches_created      boolean,
     deadline_time_game_offset   int,
     overrides                   jsonb,
     chip_plays                  jsonb,
     top_element_info            jsonb
 ));



