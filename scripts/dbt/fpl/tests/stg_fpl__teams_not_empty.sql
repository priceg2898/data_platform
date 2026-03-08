select 1
from {{ ref('stg_fpl__teams') }}
having count(*) = 0