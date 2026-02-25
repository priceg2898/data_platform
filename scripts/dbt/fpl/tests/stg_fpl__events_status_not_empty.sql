select 1
from {{ ref('stg_fpl__events_status') }}
having count(*) = 0