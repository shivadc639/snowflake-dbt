{% set configs = 
    [
        {
            "table": "SNOWFLAKE_DBT_PRACTISE_DB.DBT_SCHEMA_SILVER.CALL_CENTER_SILVER",
            "columns": "cc_silver.*",
            "table_alias": "cc_silver" 
        },
        {
            "table": "SNOWFLAKE_DBT_PRACTISE_DB.DBT_SCHEMA_SILVER.CUSTOMERS_SILVER",
            "columns": "c_customer_sk, c_customer_id, full_name, c_preferred_cust_flag, birth_year, c_birth_country, c_login, c_email_address, c_last_review_date, age, age_group",
            "table_alias": "cust_silver",
            "join_condition": "cc_silver.cc_call_center_sk = cust_silver.c_customer_sk"
        },
        {
            "table": "SNOWFLAKE_DBT_PRACTISE_DB.DBT_SCHEMA_SILVER.INVENTORY_SILVER",
            "columns": "inv_item_sk, inv_warehouse_sk, cnt",
            "table_alias": "inv_silver",
            "join_condition": "cust_silver.c_customer_sk = inv_silver.inv_item_sk"
        }
    ]
%}

SELECT
    {%for config in configs%}
        {{config['columns']}} {% if not loop.last %},{%endif%}
    {%endfor%}
FROM
    {% for config in configs %}
    {% if loop.first %}
        {{config['table']}} as {{config['table_alias']}}
    {% else %}
        LEFT JOIN {{config['table']}} as {{config['table_alias']}}
        ON {{config['join_condition']}}
    {%endif%}
    {%endfor%}