select
    {{ dbt_utils.generate_surrogate_key(['provider_ccn']) }} as provider_key,
    provider_ccn,
    provider_name,
    city,
    state_code,
    zip_code,
    ruca_code,
    ruca_description,
    last_reported_year
from {{ ref('int_providers__latest') }}
