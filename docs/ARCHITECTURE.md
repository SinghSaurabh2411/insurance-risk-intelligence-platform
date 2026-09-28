# Architecture

## End-to-end flow

```text
SOURCE CSV
    |
    v
DWH_BRONZE.BRONZE_POLICY_DATA
    |
    v
DWH_SILVER
    |
    v
DWH_GOLD
    |
    v
Future analytics / API / GenAI
```

## Bronze

Bronze is append-oriented. File-level SHA-256 identifies source-file versions; `RECORD_HASH` fingerprints source/business columns excluding audit columns. `ETL_CONTROL` prevents reloading an already successful filename/hash pair.

## Silver

Exactly eight business tables are used:

```text
SILVER_RECORD
SILVER_TIME
SILVER_POLICY
SILVER_CUSTOMER
SILVER_PRODUCT
SILVER_CHANNEL
SILVER_COVERAGE
SILVER_FINANCIAL
```

`SILVER_STAGE` is technical staging only. Observation-level Silver tables preserve `(ID_POLICY, ID_INSURED, PERIOD)`. Silver persistence is Oracle MERGE/upsert at that grain.

## Gold star schema

- **DIM_TIME:** one row per `PERIOD`; surrogate `TIME_KEY`.
- **DIM_CUSTOMER:** one row per `(ID_POLICY, ID_INSURED)`; surrogate `CUSTOMER_KEY`.
- **DIM_POLICY:** one row per `ID_POLICY`; surrogate `POLICY_KEY`.
- **DIM_PRODUCT:** one row per `(TYPE_PRODUCT, REIMBURSEMENT)`; surrogate `PRODUCT_KEY`.
- **DIM_CHANNEL:** one row per `DISTRIBUTION_CHANNEL`; surrogate `CHANNEL_KEY`.
- **FACT_POLICY:** one row per `(ID_POLICY, ID_INSURED, PERIOD)`, with five dimension foreign keys, measures, observation-state attributes, and lineage/audit fields.

The dataset is annual, with periods 2017–2019 only.

## No FACT_CLAIMS

The source has no claim-level business entity such as claim ID, event date, type, or status. Therefore `cost_claims_year` remains a policy-period measure in `FACT_POLICY`.

## SCD strategy

Current Gold dimensions are static/Type 1 and loaded by full refresh. SCD2 is intentionally not used. A future SCD2 requirement would be an explicit architecture change.

## Technical staging

`DWH_GOLD.GOLD_STAGE` is implementation staging only and is not a business Gold object.


## Orchestration and Airflow

The repository contains a thin orchestration layer in `src/orchestration/pipeline.py` and an Airflow DAG in `dags/insurance_risk_intelligence_pipeline.py`.

The execution contract is:

```text
BRONZE -> SILVER -> GOLD
```

The Airflow DAG is configured with `bronze >> silver >> gold`, `catchup=False`, `max_active_runs=1`, and `schedule=None`. It was manually triggered and completed successfully. Airflow does not duplicate layer-specific ETL logic; it invokes the existing Bronze, Silver, and Gold loaders.
