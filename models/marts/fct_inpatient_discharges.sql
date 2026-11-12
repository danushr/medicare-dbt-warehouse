{{
    config(
        materialized='incremental',
        unique_key='discharge_key',
        incremental_strategy='delete+insert',
        on_schema_change='fail'
    )
}}

select
    {{ dbt_utils.generate_surrogate_key(['provider_ccn', 'drg_code', 'data_year']) }} as discharge_key,
    {{ dbt_utils.generate_surrogate_key(['provider_ccn']) }} as provider_key,
    {{ dbt_utils.generate_surrogate_key(['drg_code']) }} as drg_key,
    data_year,
    total_discharges,
    avg_covered_charges,
    avg_total_payment,
    avg_medicare_payment,
    cast(total_discharges * avg_medicare_payment as decimal(18, 2)) as total_medicare_payment
from {{ ref('stg_cms__inpatient') }}

{% if is_incremental() %}
where data_year > (select coalesce(max(data_year), 0) from {{ this }})
{% endif %}
