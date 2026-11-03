# Medallion Architecture

## Purpose

This document describes the implemented Bronze, Silver and Gold layers based on the repository's SQL DDL and Python ETL code.

## End-to-end layers

```text
CSV source
   |
   v
BRONZE_POLICY_DATA
   |
   v
Eight Silver business projections
   |
   v
Five Gold dimensions + FACT_POLICY
```

## Bronze layer

Target: `DWH_BRONZE.BRONZE_POLICY_DATA`.

The Bronze pipeline discovers CSV files, reads them without schema inference, validates the source, applies typed transformations, generates row-level record hash and audit fields, and writes to Oracle using the configured append mode.

The complete source file is hashed with SHA-256. File-level incremental detection checks the successful filename/hash pair in `ETL_CONTROL`. A changed file with a different content hash is treated as a different file version by this mechanism. This is not a record-level MERGE.

## Silver layer

The implemented Silver model contains exactly eight business tables:

1. `SILVER_RECORD`
2. `SILVER_TIME`
3. `SILVER_POLICY`
4. `SILVER_CUSTOMER`
5. `SILVER_PRODUCT`
6. `SILVER_CHANNEL`
7. `SILVER_COVERAGE`
8. `SILVER_FINANCIAL`

Observation-level targets use `(ID_POLICY, ID_INSURED, PERIOD)`. `SILVER_TIME` contains only `PERIOD` and uses that single column as its key. Policy lifecycle year attributes reside in `SILVER_POLICY`; insured lifecycle year attributes reside in `SILVER_CUSTOMER`; `COST_CLAIMS_YEAR` resides in `SILVER_FINANCIAL`.

`SILVER_STAGE` is a technical staging table, not an additional business table. Silver persistence is implemented through Oracle MERGE statements.

## Gold layer

The implemented Gold star schema consists of:

**Dimensions**
- `DIM_TIME`: unique `PERIOD`.
- `DIM_CUSTOMER`: unique `(ID_POLICY, ID_INSURED)`.
- `DIM_POLICY`: unique `ID_POLICY`.
- `DIM_PRODUCT`: unique `(TYPE_PRODUCT, REIMBURSEMENT)`.
- `DIM_CHANNEL`: unique `DISTRIBUTION_CHANNEL`.

**Fact**
- `FACT_POLICY`: one row per `(ID_POLICY, ID_INSURED, PERIOD)`.

The fact stores five dimension foreign keys, the business key, policy-period measures, selected observation attributes and lineage fields. `COST_CLAIMS_YEAR` is a measure in `FACT_POLICY`; the current model does not define a claim-level fact. There is no `FACT_CLAIMS` table in the current DDL or loader.

The Gold loader clears and reloads the dimensions and fact. Gold is therefore currently full-refresh, not Delta Lake MERGE and not SCD Type 2. Dimension selection uses the latest observation period for customer and policy keys; product, channel and time use distinct values.

`GOLD_STAGE` is technical staging only.

## Pipeline execution

The Python orchestration sequence is Bronze -> Silver -> Gold. The Airflow DAG expresses the same task dependency. Its current configuration is manual/unscheduled (`schedule=None`), with `catchup=False` and `max_active_runs=1`.

## Downstream application boundary

FastAPI and Streamlit source code exists in the repository. The dashboard consumes the API client rather than implementing a separate direct-Oracle data path. RAG and NL2SQL are not included as implemented components in the current warehouse ETL code.

## Implementation principles evidenced by code

- Bronze file-level idempotency is based on source filename and complete-file SHA-256.
- Silver MERGE keys are explicit in the merge implementation.
- Gold is rebuilt by the current loader.
- The warehouse business observation grain is preserved in Silver and the fact.
- Staging objects are kept distinct from business tables.
