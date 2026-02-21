select c_customer_sk,
       c_customer_id,
       concat(c_salutation, ' ', c_first_name, ' ', c_last_name) full_name,
       c_preferred_cust_flag,
       date_from_parts(c_birth_year, c_birth_month, c_birth_day) as birth_year,
       c_birth_country,
       c_login,
       c_email_address,
       c_last_review_date,
       age,
       case when age < 20 then 'Young'
            when age >= 21 and age <= 50 then 'middle'
            when age >= 51 and age <= 90 then 'old' end
       age_group from
(select 
*,
year(current_date()) - c_birth_year as age
from {{ref('bronze_customer')}})

