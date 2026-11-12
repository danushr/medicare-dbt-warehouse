select
    drg_code,
    drg_description,
    data_year as last_reported_year
from {{ ref('stg_cms__inpatient') }}
qualify row_number() over (partition by drg_code order by data_year desc, provider_ccn) = 1
