# Data Dictionary

## Purpose and authority

This document describes the implemented warehouse structures and the mappings visible in the committed SQL DDL and Python transformations. The SQL DDL defines Oracle table structures and constraints; the Python projection and transformation code defines the columns selected and the transformation behavior.

The accompanying Excel workbook is retained as source-level metadata. This Markdown document is the implementation-aligned warehouse reference. Where a business definition, unit, or source meaning is not established by code or DDL, it is not inferred here.

## Warehouse layers

| Layer | Implemented object / behavior |
|---|---|
| Bronze | `DWH_BRONZE.BRONZE_POLICY_DATA`; source CSV ingestion, technical transformations, audit/record hash fields, append write mode |
| Silver | Eight business projections, persisted to Oracle using MERGE |
| Gold | Five dimensions and one fact table; Gold loader clears and rebuilds the analytical tables (full refresh) |

## Business observation grain

The observation-level business key used by Silver and FACT_POLICY is:

```text
(ID_POLICY, ID_INSURED, PERIOD)
```

## Bronze

The committed Bronze loader reads source CSV files with schema inference disabled, validates and transforms them, calculates a file SHA-256, generates record/audit fields, and writes to `DWH_BRONZE.BRONZE_POLICY_DATA` using the configured Bronze write mode. The repository's configured write mode and DDL/code must be consulted for exact deployment configuration; the implementation uses append persistence.

File-level duplicate detection uses the source filename and complete-file SHA-256 in `ETL_CONTROL`. `RECORD_HASH` is a separate row-level fingerprint. These hashes serve different purposes.

## Silver business tables

The projection definitions in `src/silver/silver_transform.py` and the corresponding DDL files define these eight business tables:

| Table | Projected columns | Grain |
|---|---|---|
| `SILVER_RECORD` | `ID, ID_POLICY, ID_INSURED, PERIOD, RECORD_HASH, LOAD_ID, LOAD_TIMESTAMP, SOURCE_FILE, ETL_CREATED_BY` | `(ID_POLICY, ID_INSURED, PERIOD)` |
| `SILVER_TIME` | `PERIOD` | One row per distinct `PERIOD` |
| `SILVER_POLICY` | `ID_POLICY, ID_INSURED, PERIOD, DATE_EFFECT_POLICY, DATE_LAPSE_POLICY, YEAR_EFFECT_POLICY, YEAR_LAPSE_POLICY, SENIORITY_POLICY, TYPE_POLICY, TYPE_POLICY_DG, NEW_BUSINESS, LAPSE` | `(ID_POLICY, ID_INSURED, PERIOD)` |
| `SILVER_CUSTOMER` | `ID_INSURED, ID_POLICY, PERIOD, DATE_EFFECT_INSURED, DATE_LAPSE_INSURED, YEAR_EFFECT_INSURED, YEAR_LAPSE_INSURED, SENIORITY_INSURED, GENDER, AGE` | `(ID_POLICY, ID_INSURED, PERIOD)` |
| `SILVER_PRODUCT` | `ID_POLICY, ID_INSURED, PERIOD, TYPE_PRODUCT, REIMBURSEMENT` | `(ID_POLICY, ID_INSURED, PERIOD)` |
| `SILVER_CHANNEL` | `ID_POLICY, ID_INSURED, PERIOD, DISTRIBUTION_CHANNEL` | `(ID_POLICY, ID_INSURED, PERIOD)` |
| `SILVER_COVERAGE` | `ID_POLICY, ID_INSURED, PERIOD, EXPOSURE_TIME, N_MEDICAL_SERVICES` | `(ID_POLICY, ID_INSURED, PERIOD)` |
| `SILVER_FINANCIAL` | `ID_POLICY, ID_INSURED, PERIOD, PREMIUM, COST_CLAIMS_YEAR` | `(ID_POLICY, ID_INSURED, PERIOD)` |

`SILVER_STAGE` is a technical staging table used by the Silver load path; it is not a ninth business subject table.

Important implemented placements:
- Policy lifecycle year fields are in `SILVER_POLICY`.
- Insured lifecycle year fields are in `SILVER_CUSTOMER`.
- `SILVER_TIME` contains only `PERIOD`.
- `COST_CLAIMS_YEAR` is in `SILVER_FINANCIAL`; no claim-level Silver table is defined.

The Silver merge implementation uses `(ID_POLICY, ID_INSURED, PERIOD)` for observation-level targets and `PERIOD` for `SILVER_TIME`.

## Gold dimensions

The DDL in `Database/17_CREATE_GOLD_DIMENSIONS.sql` defines:

| Dimension | Business key / uniqueness | Attributes selected by Gold transform |
|---|---|---|
| `DIM_TIME` | `PERIOD` | `PERIOD` |
| `DIM_CUSTOMER` | `(ID_POLICY, ID_INSURED)` | `DATE_EFFECT_INSURED, DATE_LAPSE_INSURED, YEAR_EFFECT_INSURED, YEAR_LAPSE_INSURED, GENDER` |
| `DIM_POLICY` | `ID_POLICY` | `TYPE_POLICY, TYPE_POLICY_DG, DATE_EFFECT_POLICY, DATE_LAPSE_POLICY, YEAR_EFFECT_POLICY, YEAR_LAPSE_POLICY` |
| `DIM_PRODUCT` | `(TYPE_PRODUCT, REIMBURSEMENT)` | `TYPE_PRODUCT, REIMBURSEMENT` |
| `DIM_CHANNEL` | `DISTRIBUTION_CHANNEL` | `DISTRIBUTION_CHANNEL` |

The Gold transform selects the latest `PERIOD` row for each `(ID_POLICY, ID_INSURED)` customer key and each `ID_POLICY` policy key. Product, channel, and time dimension inputs are distinct combinations/periods. Surrogate keys are assigned in the Gold loader.

## Gold fact

Only `FACT_POLICY` is defined in the committed Gold DDL. Its primary/business grain is `(ID_POLICY, ID_INSURED, PERIOD)`. It contains five dimension keys, the three business-key columns, measures and observation attributes, plus load/source lineage fields.

Measures and attributes defined by `Database/18_CREATE_GOLD_FACT_POLICY.sql`:
- `PREMIUM`
- `COST_CLAIMS_YEAR`
- `EXPOSURE_TIME`
- `N_MEDICAL_SERVICES`
- `AGE`
- `SENIORITY_POLICY`
- `SENIORITY_INSURED`
- `NEW_BUSINESS`
- `LAPSE`

Lineage fields: `LOAD_ID, LOAD_TIMESTAMP, SOURCE_FILE, RECORD_HASH, ETL_CREATED_BY`.

There is no `FACT_CLAIMS` table in the committed Gold DDL or Gold loader.

## Technical staging

- `DWH_SILVER.SILVER_STAGE`: Silver staging object.
- `DWH_GOLD.GOLD_STAGE`: Gold staging object.

These are technical load objects, not additional business subject areas or dimensions/facts.

## Components outside the warehouse

The repository also contains Python implementation for orchestration, FastAPI and Streamlit. Their details belong in the corresponding operational documentation. RAG/NL2SQL are not described here as implemented warehouse components.

## Scope limitation

This document intentionally does not invent business definitions, units, domain constraints, or transformation rules not explicitly present in the source code or DDL. Refer to source metadata for definitions and validate any ambiguous source semantics before using them in analytics or retrieval.
