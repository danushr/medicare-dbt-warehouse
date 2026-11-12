select s.provider_ccn, s.drg_code, s.data_year
from {{ ref('stg_cms__inpatient') }} as s
left join {{ ref('fct_inpatient_discharges') }} as f
    on f.discharge_key = {{ dbt_utils.generate_surrogate_key(['s.provider_ccn', 's.drg_code', 's.data_year']) }}
where f.discharge_key is null
