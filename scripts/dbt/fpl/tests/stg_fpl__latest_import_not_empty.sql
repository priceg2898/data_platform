select 1
from {{ ref('stg_fpl__latest_import') }}
having count(*) = 0