{% set cols = ['C_CUSTOMER_SK','C_CUSTOMER_ID','C_BIRTH_DAY', 'C_BIRTH_YEAR', 'C_BIRTH_COUNTRY'] %}

select
{% for col in cols %}
    {{col}}
    {%if not loop.last%}, {%endif%} ---removes ',' at the last column
{%endfor%}
from {{ref('bronze_customer')}}