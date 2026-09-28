# Insurance Risk Intelligence Platform — Project Handoff

**Status:** Frozen post-Gold + Airflow validation state  
**Repository:** SinghSaurabh2411/insurance-risk-intelligence-platform  
**Validated through:** Bronze → Silver → Gold → Airflow orchestration  
**Latest implementation baseline:** f07ac0ef74e8bcf4be27847ad8b314ba58c5da72

## Authority rules

- GitHub `main` and repository code/Oracle DDL are implementation authority.
- Documentation records design intent and validated execution evidence.
- Never call a layer implemented without code/DDL and execution evidence.
- Preserve frozen naming and business grain unless explicitly changed.
- Do not claim tests/execution passed without evidence.
- Keep credentials and local JDBC drivers out of Git.

## Architecture

```text
SOURCE CSV
    |
    v
BRONZE
    |
    v
SILVER
    |
    v
GOLD
    |
    v
Future analytics / API / AI
```

Schemas:

```text
DWH_CONTROL
DWH_BRONZE
DWH_SILVER
DWH_GOLD
```

Frozen business grain:

```text
(ID_POLICY, ID_INSURED, PERIOD)
```

## Bronze — implemented, validated, frozen

Target:

```text
DWH_BRONZE.BRONZE_POLICY_DATA
```

Strategy:

- file-level SHA-256 source-file detection
- append loading
- `RECORD_HASH` over all source/business columns excluding audit columns
- `ETL_CONTROL` checks source filename + source hash + SUCCESS status
- same filename with a different hash is a new source version
- no record-level MERGE

Final validated count:

```text
228,711
```

Final source is `BASE_DATA.csv`. `policy_test.csv` was removed because it introduced duplicate business-grain observations.

## Silver — implemented, validated, frozen

Exactly eight business tables:

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

Technical staging:

```text
DWH_SILVER.SILVER_STAGE
```

Silver uses Oracle MERGE/upsert at `(ID_POLICY, ID_INSURED, PERIOD)`. It is not SCD2.

Validated:

- 228,711 Bronze rows
- all eight Silver DQ checks passed
- all eight MERGEs succeeded
- Bronze/Silver reconciliation = 0 both directions
- observation-key integrity = 0 invalid keys
- rerun/idempotency validated
- periods = 2017, 2018, 2019

## Gold — implemented, validated, frozen

Frozen star schema:

```text
DIM_TIME
DIM_CUSTOMER
DIM_POLICY
DIM_PRODUCT
DIM_CHANNEL
FACT_POLICY
```

There is **no FACT_CLAIMS** because the source has no claim-level business entity. `cost_claims_year` remains a policy-period financial measure.

### Gold grains

```text
DIM_TIME      -> PERIOD
DIM_CUSTOMER  -> (ID_POLICY, ID_INSURED)
DIM_POLICY    -> ID_POLICY
DIM_PRODUCT   -> (TYPE_PRODUCT, REIMBURSEMENT)
DIM_CHANNEL   -> DISTRIBUTION_CHANNEL
FACT_POLICY   -> (ID_POLICY, ID_INSURED, PERIOD)
```

Surrogate keys:

```text
TIME_KEY
CUSTOMER_KEY
POLICY_KEY
PRODUCT_KEY
CHANNEL_KEY
```

Gold currently uses deterministic surrogate keys and a full-refresh load. No SCD2 is used.

### Gold implementation

```text
Database/17_CREATE_GOLD_DIMENSIONS.sql
Database/18_CREATE_GOLD_FACT_POLICY.sql
Database/19_CREATE_GOLD_STAGE.sql
Database/20_CREATE_GOLD_INDEXES.sql
Database/21_GOLD_DQ_CHECKS.sql

src/gold/gold_transform.py
src/gold/gold_loader.py
```

`GOLD_STAGE` is technical staging only.

### Gold execution evidence

Complete Bronze → Silver → Gold execution succeeded.

```text
FACT_POLICY = 228,711
```

A Spark temporary-directory cleanup error appeared after successful pipeline completion during shutdown cleanup. It did not indicate a Gold data-load failure.

### Gold validation evidence

```text
FACT_POLICY rows                    228,711
Distinct fact business keys        228,711
Duplicate fact keys                     0

DIM_TIME                                  3
DIM_CUSTOMER                        100,453
DIM_POLICY                           45,162
DIM_PRODUCT                               5
DIM_CHANNEL                               3

Dimension business-key duplicates         0
Invalid fact foreign keys                 0
SILVER_NOT_IN_GOLD                        0
GOLD_NOT_IN_SILVER                        0
NULL fact dimension/business keys         0
```

Fact periods:

```text
2017 = 78,459
2018 = 73,970
2019 = 76,282
```

Measure reconciliation:

```text
PREMIUM
  Silver = 194864832.58909062
  Gold   = 194864832.6043
  Difference = 0.01520938

COST_CLAIMS_YEAR
  Difference = 0

EXPOSURE_TIME
  Difference = 0.000007009

N_MEDICAL_SERVICES
  Difference = 0
```

The Premium and Exposure differences are very small numeric precision/scale effects from Gold Oracle numeric definitions. Grain, row counts, keys, and the remaining measures reconcile exactly.

## Current frozen status

```text
BRONZE
  implemented / validated / frozen

SILVER
  implemented / DQ validated / reconciled / rerun validated / frozen

GOLD
  implemented / DQ validated / grain reconciled /
  FK validated / measure reconciled within numeric precision tolerance /
  frozen

ORCHESTRATION
  implemented / stage sequencing and fail-fast behavior

AIRFLOW DAG
  implemented / manual runtime execution validated

FASTAPI
  planned / not implemented

STREAMLIT
  planned / not implemented

RAG / VECTOR DB / LLM
  planned / not implemented
```

## Orchestration — implemented and runtime validated

The repository now contains a thin orchestration layer that sequences the frozen stages without moving layer-specific transformation or persistence logic:

```text
BRONZE -> SILVER -> GOLD
```

Implementation:

```text
src/orchestration/pipeline.py
src/orchestration/__init__.py
dags/insurance_risk_intelligence_pipeline.py
```

The normal `src.main` entry point now delegates to the orchestration layer.

The Airflow DAG is configured as `bronze >> silver >> gold`, with `catchup=False` and `max_active_runs=1`. It intentionally has no production schedule yet.

Airflow runtime execution has been **manually triggered and completed successfully**. This is current execution evidence for the Airflow orchestration layer.

## Next sequence

The next work is:

```text
1. API / analytics interfaces
2. GenAI / RAG capabilities
```

Do not recreate or re-profile frozen Bronze, Silver, or Gold unless a concrete implementation defect is found.

## Final principles

- Business grain remains `(ID_POLICY, ID_INSURED, PERIOD)`.
- Bronze remains append + source-file SHA-256 detection + complete RECORD_HASH.
- Silver remains eight business tables + technical stage + DQ + Oracle MERGE/upsert.
- Gold remains five dimensions + FACT_POLICY + technical stage + full refresh.
- No FACT_CLAIMS.
- No SCD2 in current Silver or Gold implementation.
- Airflow is an orchestration layer, currently validated by a successful manual run and intentionally unscheduled.
- No credentials in Git.
