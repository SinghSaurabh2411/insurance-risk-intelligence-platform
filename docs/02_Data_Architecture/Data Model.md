# Data Model

## Purpose

This document describes the Oracle warehouse model defined by the committed SQL DDL and the mappings implemented in the Python transformation code.

## Observation grain

The observation-level business key used by Silver and `FACT_POLICY` is:

```text
(ID_POLICY, ID_INSURED, PERIOD)
```

## Bronze

Table: `DWH_BRONZE.BRONZE_POLICY_DATA`.

The Bronze table stores source observations together with the technical and lineage columns created by the Bronze pipeline. The source is CSV. File-level duplicate detection uses `SOURCE_FILE` and the SHA-256 of the complete source file; row-level `RECORD_HASH` is a separate field.

## Silver model

There are eight Silver business tables. Seven are observation-level subject projections plus the technical record projection; `SILVER_TIME` is period-level.

| Table | Grain / primary key | Columns selected by Python projection |
|---|---|---|
| `SILVER_RECORD` | `(ID_POLICY, ID_INSURED, PERIOD)` | `ID, ID_POLICY, ID_INSURED, PERIOD, RECORD_HASH, LOAD_ID, LOAD_TIMESTAMP, SOURCE_FILE, ETL_CREATED_BY` |
| `SILVER_TIME` | `PERIOD` | `PERIOD` |
| `SILVER_POLICY` | `(ID_POLICY, ID_INSURED, PERIOD)` | `ID_POLICY, ID_INSURED, PERIOD, DATE_EFFECT_POLICY, DATE_LAPSE_POLICY, YEAR_EFFECT_POLICY, YEAR_LAPSE_POLICY, SENIORITY_POLICY, TYPE_POLICY, TYPE_POLICY_DG, NEW_BUSINESS, LAPSE` |
| `SILVER_CUSTOMER` | `(ID_POLICY, ID_INSURED, PERIOD)` | `ID_INSURED, ID_POLICY, PERIOD, DATE_EFFECT_INSURED, DATE_LAPSE_INSURED, YEAR_EFFECT_INSURED, YEAR_LAPSE_INSURED, SENIORITY_INSURED, GENDER, AGE` |
| `SILVER_PRODUCT` | `(ID_POLICY, ID_INSURED, PERIOD)` | `ID_POLICY, ID_INSURED, PERIOD, TYPE_PRODUCT, REIMBURSEMENT` |
| `SILVER_CHANNEL` | `(ID_POLICY, ID_INSURED, PERIOD)` | `ID_POLICY, ID_INSURED, PERIOD, DISTRIBUTION_CHANNEL` |
| `SILVER_COVERAGE` | `(ID_POLICY, ID_INSURED, PERIOD)` | `ID_POLICY, ID_INSURED, PERIOD, EXPOSURE_TIME, N_MEDICAL_SERVICES` |
| `SILVER_FINANCIAL` | `(ID_POLICY, ID_INSURED, PERIOD)` | `ID_POLICY, ID_INSURED, PERIOD, PREMIUM, COST_CLAIMS_YEAR` |

The SQL DDL files `Database/05_CREATE_SILVER_RECORD.sql` through `Database/12_CREATE_SILVER_FINANCIAL.sql` define these tables. `SILVER_STAGE` is a technical staging object, not a ninth business table.

### Key placement

- `YEAR_EFFECT_POLICY` and `YEAR_LAPSE_POLICY` are policy attributes in `SILVER_POLICY`.
- `YEAR_EFFECT_INSURED` and `YEAR_LAPSE_INSURED` are insured attributes in `SILVER_CUSTOMER`.
- `SILVER_TIME` contains only `PERIOD`.
- `COST_CLAIMS_YEAR` is stored in `SILVER_FINANCIAL`; it is not evidence of a claim-level entity.

### Silver persistence

`src/silver/silver_merge.py` generates Oracle MERGE statements. Observation-level tables use the three-column observation key; `SILVER_TIME` uses `PERIOD`. This is the implemented merge behavior; it should not be described as SCD Type 2.

## Gold star schema

The DDL defines five dimensions and one fact.

| Object | Business key / grain | Key attributes |
|---|---|---|
| `DIM_TIME` | `PERIOD` | `TIME_KEY, PERIOD` |
| `DIM_CUSTOMER` | `(ID_POLICY, ID_INSURED)` | insured effective/lapse dates and years, gender |
| `DIM_POLICY` | `ID_POLICY` | policy type/classification, effective/lapse dates and years |
| `DIM_PRODUCT` | `(TYPE_PRODUCT, REIMBURSEMENT)` | product type, reimbursement |
| `DIM_CHANNEL` | `DISTRIBUTION_CHANNEL` | distribution channel |
| `FACT_POLICY` | `(ID_POLICY, ID_INSURED, PERIOD)` | five dimension keys, measures, observation attributes and lineage |

### Dimension row selection

The Gold transformation selects the latest `PERIOD` row for each customer key `(ID_POLICY, ID_INSURED)` and policy key `ID_POLICY`. Product and channel dimensions are built from distinct business-attribute combinations; time is built from distinct periods.

This describes the code's selection rule; it does not claim historical SCD tracking.

### FACT_POLICY

The fact contains:
- Foreign keys: `POLICY_KEY, CUSTOMER_KEY, PRODUCT_KEY, CHANNEL_KEY, TIME_KEY`.
- Business key: `ID_POLICY, ID_INSURED, PERIOD`.
- Measures: `PREMIUM, COST_CLAIMS_YEAR, EXPOSURE_TIME, N_MEDICAL_SERVICES`.
- Other selected attributes: `AGE, SENIORITY_POLICY, SENIORITY_INSURED, NEW_BUSINESS, LAPSE`.
- Lineage: `LOAD_ID, LOAD_TIMESTAMP, SOURCE_FILE, RECORD_HASH, ETL_CREATED_BY`.

There is no `FACT_CLAIMS` table in the committed Gold DDL or loader.

## Technical staging

`DWH_SILVER.SILVER_STAGE` and `DWH_GOLD.GOLD_STAGE` support loading. They are not business entities in the Silver or Gold model.

## Load patterns

- Bronze: append persistence with file-level source-version detection.
- Silver: Oracle MERGE at the defined target keys.
- Gold: current loader clears the Gold fact/dimension tables and rebuilds them; this is a full refresh.

No SCD Type 2 implementation is defined by the current Gold transformation or DDL.
