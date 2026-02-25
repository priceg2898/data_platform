WITH fixtures

AS (

SELECT
    f.*,
    stat_item ->> 'identifier' AS identifier,
    'a' AS side,
    a_elem ->> 'element' AS element,
    a_elem ->> 'value' AS value
FROM {{ref('stg_fpl__fixtures_non_flatterned')}} f
CROSS JOIN LATERAL jsonb_array_elements(f.stats::jsonb) AS stat_item
CROSS JOIN LATERAL jsonb_array_elements(stat_item -> 'a') AS a_elem

UNION ALL

SELECT
    f.*,
    stat_item ->> 'identifier' AS identifier,
    'h' AS side,
    h_elem ->> 'element' AS element,
    h_elem ->> 'value' AS value
FROM {{ref('stg_fpl__fixtures_non_flatterned')}} f
CROSS JOIN LATERAL jsonb_array_elements(f.stats::jsonb) AS stat_item
CROSS JOIN LATERAL jsonb_array_elements(stat_item -> 'h') AS h_elem

)

select * from fixtures