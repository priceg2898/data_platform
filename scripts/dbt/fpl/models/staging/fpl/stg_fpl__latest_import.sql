{{ config(
    materialized='ephemeral'
) }}

WITH latest_import AS (
    SELECT *
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY endpoint ORDER BY imported_at DESC) AS rn
        FROM fpl_api__raw_landing
    ) t
    WHERE rn = 1
)

SELECT * FROM latest_import