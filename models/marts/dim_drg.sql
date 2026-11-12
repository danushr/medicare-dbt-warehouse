select
    {{ dbt_utils.generate_surrogate_key(['drg_code']) }} as drg_key,
    drg_code,
    drg_description,
    last_reported_year
from {{ ref('int_drgs__latest') }}
