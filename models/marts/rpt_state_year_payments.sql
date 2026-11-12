select
    p.state_code,
    f.data_year,
    cast(count(distinct f.provider_key) as integer) as hospitals,
    cast(sum(f.total_discharges) as bigint) as total_discharges,
    cast(sum(f.total_medicare_payment) as decimal(18, 2)) as total_medicare_payment,
    cast(sum(f.total_medicare_payment) / sum(f.total_discharges) as decimal(18, 2)) as medicare_payment_per_discharge
from {{ ref('fct_inpatient_discharges') }} as f
inner join {{ ref('dim_provider') }} as p on f.provider_key = p.provider_key
group by p.state_code, f.data_year
