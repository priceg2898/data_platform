SELECT
    rl.imported_at,
    rl.id AS import_id,
    endpoint AS api_endpoint,
    f.id,
    f.code,
    f.event,
    f.stats,
    f.team_a,
    f.team_h,
    f.minutes,
    -- started can be timestamp or boolean, so keep as text first
    CASE
        WHEN f.started ~ '^\d{4}-\d{2}-\d{2}' THEN f.started::timestamptz
        ELSE NULL
    END AS started,
    f.finished,
    f.pulse_id,
    CASE
        WHEN f.kickoff_time ~ '^\d{4}-\d{2}-\d{2}' THEN f.kickoff_time::timestamptz
        ELSE NULL
    END AS kickoff_time,
    f.team_a_score,
    f.team_h_score,
    f.team_a_difficulty,
    f.team_h_difficulty,
    f.finished_provisional,
    f.provisional_start_time
FROM bronze__raw_landing rl,
LATERAL jsonb_array_elements(raw_json) AS f_item,
LATERAL jsonb_to_record(f_item) AS f(
    id int,
    code int,
    event int,
    stats jsonb,
    team_a int,
    team_h int,
    minutes int,
    started text,                -- text instead of timestamptz
    finished boolean,
    pulse_id int,
    kickoff_time text,           -- text instead of timestamptz
    team_a_score int,
    team_h_score int,
    team_a_difficulty int,
    team_h_difficulty int,
    finished_provisional boolean,
    provisional_start_time boolean
)
WHERE endpoint = 'fixtures/'