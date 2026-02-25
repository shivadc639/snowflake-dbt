{% set birth_country_flag = 'INDIA' %}

{% if birth_country_flag == 'FRANCE' %}
    {% set birth_year_flag = 1944  %}
{% else %}
    {% set birth_year_flag = 1947 %}
{% endif %}

select * from {{ref('bronze_customer')}} 
where C_BIRTH_COUNTRY = '{{birth_country_flag}}'
and C_BIRTH_YEAR = {{birth_year_flag}}

---{%set flag  = 1%}

---select * from {{ref('bronze_customer')}}
---{%if flag == 1%}
---    WHERE C_BIRTH_YEAR = 1944
---{% else %}
    ---WHERE C_BIRTH_YEAR = 1947
---{% endif %}