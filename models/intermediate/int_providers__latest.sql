select
    provider_ccn,
    provider_name,
    city,
    state_code,
    zip_code,
    ruca_code,
    ruca_description,
    data_year as last_reported_year
from {{ ref('stg_cms__inpatient') }}
qualify row_number() over (partition by provider_ccn order by data_year desc, drg_code) = 1
