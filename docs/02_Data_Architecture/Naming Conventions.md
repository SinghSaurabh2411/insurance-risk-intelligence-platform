# Naming Conventions

## Purpose

This document records naming patterns visible in the committed SQL DDL and Python code. It is not a proposal for renaming existing objects.

## Oracle schemas and objects

The warehouse uses schema-qualified objects including:
- `DWH_BRONZE.BRONZE_POLICY_DATA`
- `DWH_SILVER` Silver business tables and `SILVER_STAGE`
- `DWH_GOLD` dimensions, `FACT_POLICY`, and `GOLD_STAGE`
- `ETL_CONTROL` for file/load control metadata, as configured in the Python control-table module.

## Layer prefixes

| Layer | Naming pattern | Examples |
|---|---|---|
| Bronze | `BRONZE_*` | `BRONZE_POLICY_DATA` |
| Silver | `SILVER_*` | `SILVER_RECORD`, `SILVER_FINANCIAL` |
| Gold dimensions | `DIM_*` | `DIM_POLICY`, `DIM_CUSTOMER` |
| Gold fact | `FACT_*` | `FACT_POLICY` |
| Technical staging | layer-specific `*_STAGE` | `SILVER_STAGE`, `GOLD_STAGE` |

## Keys

Observation-level business keys are:
`ID_POLICY, ID_INSURED, PERIOD`.

The Silver merge implementation uses those three columns for observation-level tables and `PERIOD` for `SILVER_TIME`.

Gold surrogate key names defined by the DDL:
- `TIME_KEY`
- `CUSTOMER_KEY`
- `POLICY_KEY`
- `PRODUCT_KEY`
- `CHANNEL_KEY`

Gold dimension business keys are:
- `DIM_TIME`: `PERIOD`
- `DIM_CUSTOMER`: `ID_POLICY, ID_INSURED`
- `DIM_POLICY`: `ID_POLICY`
- `DIM_PRODUCT`: `TYPE_PRODUCT, REIMBURSEMENT`
- `DIM_CHANNEL`: `DISTRIBUTION_CHANNEL`

## Column naming

SQL identifiers use uppercase names in the DDL. Python source projections use the canonical source-field names and the Gold transformation selects uppercase column identifiers after reading Oracle tables through JDBC. The Silver projection code normalizes Oracle JDBC column-name casing before selecting source columns.

## Technical fields

The pipeline uses fields including `LOAD_ID`, `LOAD_TIMESTAMP`, `SOURCE_FILE`, `SOURCE_FILE_HASH`, `RECORD_HASH`, and `ETL_CREATED_BY`. Their presence and purpose must be taken from the corresponding DDL and Python modules; file-level and row-level hashes are distinct.

## Current object scope

There is no implemented `SILVER_CLAIMS`, `SILVER_ENRICHMENT`, or `FACT_CLAIMS` object in the current Silver projections/Gold DDL and loader. Do not use these names as current warehouse objects.

## Python module naming

Layer modules use names such as:
- `bronze_loader.py`, `bronze_transform.py`, `bronze_validator.py`
- `silver_loader.py`, `silver_transform.py`, `silver_merge.py`, `silver_validator.py`
- `gold_loader.py`, `gold_transform.py`

Orchestration is implemented in `src/orchestration/pipeline.py`; the Airflow DAG is `dags/insurance_risk_intelligence_pipeline.py`.
