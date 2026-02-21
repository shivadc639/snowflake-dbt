select
cc_call_center_sk,
cc_call_center_id,
cc_rec_start_date,
cc_rec_end_date,
concat (year_diff + floor(month_diff / 12) + floor(day_diff / 365), 'years', ' ',
mod(month_diff, 12), 'months', ' ', 
mod(day_diff, 365), 'days') cc_total_rec_time,
cc_name,
cc_class,
cc_employees,
abs(cc_sq_ft) cc_sq_ft,
cc_hours,
cc_mkt_id,
cc_market_manager,
cc_division,
cc_division_name, cc_company,
cc_company_name,
concat(cc_street_name, ',', cc_street_type, ',', cc_suite_number, ',', cc_city, ',', cc_county, ',', cc_state, ',', cc_zip, ',', cc_country) cc_full_address,
cc_GMT_OFFSET,
cc_tax_percentage 
from
(
select *, datediff(year, cc_rec_start_date, cc_rec_end_date) year_diff,
datediff(month, cc_rec_start_date, cc_rec_end_date) month_diff,
datediff(day, cc_rec_start_date, cc_rec_end_date) day_diff
from {{ref('bronze_call_center')}}
)