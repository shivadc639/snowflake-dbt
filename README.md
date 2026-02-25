Welcome to your new dbt project!

This project demonstrates a dbt (data build tool) pipeline built on Snowflake, using the Snowflake sample data (SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL). It transforms raw source tables (CALL_CENTER, CUSTOMER, INVENTORY) into clean, structured bronze, silver, and gold layers within a dedicated database (SNOWFLAKE_DBT_PRACTICE_DB). 

<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/45269cd9-d100-4d3b-bde7-dc8c431e3a7c" />

**Project Structure**
.
├── analyses/
├── macros/
├── models/
│   ├── bronze/
│   │   ├── bronze_call_center.sql
│   │   ├── bronze_customer.sql
│   │   └── bronze_inventory.sql
│   ├── silver/
│   │   ├── call_center_silver.sql
│   │   ├── customers_silver.sql
│   │   └── inventory_silver.sql
│   ├── gold/
│   │   └── metadata_given_configs.sql
│   └── sources/
│       └── sources.yml
├── seeds/
├── tests/
├── dbt_project.yml
└── README.md
