select *
from {{ ref('bronze__teams') }}
where id = 1
