select
    rndrng_prvdr_ccn as provider_ccn,
    trim(rndrng_prvdr_org_name) as provider_name,
    trim(rndrng_prvdr_city) as city,
    rndrng_prvdr_state_abrvtn as state_code,
    rndrng_prvdr_zip5 as zip_code,
    rndrng_prvdr_ruca as ruca_code,
    rndrng_prvdr_ruca_desc as ruca_description,
    drg_cd as drg_code,
    trim(drg_desc) as drg_description,
    data_year,
    cast(replace(tot_dschrgs, ',', '') as integer) as total_discharges,
    cast(avg_submtd_cvrd_chrg as decimal(18, 2)) as avg_covered_charges,
    cast(avg_tot_pymt_amt as decimal(18, 2)) as avg_total_payment,
    cast(avg_mdcr_pymt_amt as decimal(18, 2)) as avg_medicare_payment
from {{ source('cms', 'inpatient') }}
