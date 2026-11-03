# Data Flow

## Purpose

This document describes the implemented data movement visible in the committed Python and SQL code. It distinguishes warehouse ETL from orchestration and downstream consumption.

## Implemented end-to-end warehouse flow

```text
BASE_DATA.csv
    |
    v
PySpark Bronze ingestion / validation / transformation
    |
    v
DWH_BRONZE.BRONZE_POLICY_DATA
    |
    v
PySpark Silver projections
    |
    v
DWH_SILVER.SILVER_STAGE
    |
    v
Oracle MERGE into eight Silver business tables
    |
    v
PySpark Gold transformations
    |
    v
DWH_GOLD.GOLD_STAGE
    |
    v
Gold dimensions + FACT_POLICY (full refresh)
```

## Bronze

The Bronze loader:
1. Discovers source CSV files.
2. Calculates a complete-file SHA-256.
3. Reads CSV data with schema inference disabled.
4. Validates the source structure and data.
5. Applies Bronze transformations, including typed fields and audit/record-hash fields.
6. Writes to `DWH_BRONZE.BRONZE_POLICY_DATA`.
7. Updates `ETL_CONTROL` with `STARTED`, `SUCCESS`, or `FAILED` status.

The file handler and control-table logic use source filename plus file hash to determine whether an already-successful file version should be skipped. The complete-file SHA-256 is not the same as `RECORD_HASH`. Bronze persistence is append-oriented; it is not a record-level MERGE.

## Silver

`src/silver/silver_transform.py` defines eight projections:
- `SILVER_RECORD`
- `SILVER_TIME`
- `SILVER_POLICY`
- `SILVER_CUSTOMER`
- `SILVER_PRODUCT`
- `SILVER_CHANNEL`
- `SILVER_COVERAGE`
- `SILVER_FINANCIAL`

Observation-level tables use `(ID_POLICY, ID_INSURED, PERIOD)`. `SILVER_TIME` is distinct by `PERIOD` and has one row per period. The SQL DDL defines the corresponding target columns and primary keys.

The Silver loader writes projections to `DWH_SILVER.SILVER_STAGE`; `src/silver/silver_merge.py` then executes Oracle MERGE statements. Observation-level targets match on the three-column business key; `SILVER_TIME` matches on `PERIOD`.

## Gold

The Gold loader reads all eight Silver tables. The Gold transform:
- Selects one latest-period customer row per `(ID_POLICY, ID_INSURED)`.
- Selects one latest-period policy row per `ID_POLICY`.
- Builds distinct product, channel and period dimension inputs.
- Builds `FACT_POLICY` by joining the Silver projections on the observation grain and joining the five dimensions to obtain surrogate keys.

The Gold loader clears the existing fact/dimension targets and reloads the dimensions and fact. This is a full-refresh pattern in the current implementation. The DDL defines five dimensions and one fact table; no `FACT_CLAIMS` exists.

## Orchestration

`src/orchestration/pipeline.py` defines the stage sequence Bronze -> Silver -> Gold. The Airflow DAG in `dags/insurance_risk_intelligence_pipeline.py` defines task dependencies `bronze >> silver >> gold`. It is configured with `schedule=None`, `catchup=False`, and `max_active_runs=1`. This means the DAG is manually triggered/unscheduled by configuration; do not describe it as a scheduled production workflow.

## API and dashboard consumption

The repository contains a FastAPI service under `src/api/` and a Streamlit dashboard under `src/dashboard/`. The dashboard's API client calls the service; the dashboard is not documented as connecting directly to Oracle. Consult `docs/DASHBOARD.md` and the API source for route/security details.

RAG and NL2SQL are not part of the current implemented data flow documented by the warehouse ETL code.

## Data lineage

The fact construction carries `LOAD_ID`, `LOAD_TIMESTAMP`, `SOURCE_FILE`, `RECORD_HASH`, and `ETL_CREATED_BY` from the Silver record projection into `FACT_POLICY`. The Silver record projection itself carries these fields from Bronze.

## Implementation boundary

This document reports code/DDL behavior. It does not assert production scheduling, streaming ingestion, CDC, a separate claims entity, SCD Type 2, or unimplemented AI capabilities.
