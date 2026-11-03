# Insurance Risk Intelligence Platform — Project Handoff

**Status:** Warehouse frozen; orchestration, API and dashboard implemented  
**Repository:** SinghSaurabh2411/insurance-risk-intelligence-platform  
**Implementation reference:** current GitHub `main`; SQL DDL and Python code define implementation  
**Validation reference:** `docs/VALIDATION.md`

## Authority rules

- Inspect current GitHub `main` before continuing work; do not treat an older handoff snapshot as newer than the repository.
- SQL DDL defines Oracle structures, keys and constraints.
- Python code defines ETL projections, transformations, load patterns, API and dashboard behavior.
- Execution/validation claims must be grounded in recorded run evidence; code presence alone is not proof of successful runtime execution.
- Documentation describes the implementation and approved design intent; it must not override code/DDL.
- Do not invent business definitions, units, source semantics or behavior not evidenced by source documentation or code.
- Preserve frozen warehouse decisions unless explicitly changed by the user.

## Frozen warehouse grain

```text
(ID_POLICY, ID_INSURED, PERIOD)
```

## Bronze

Target: `DWH_BRONZE.BRONZE_POLICY_DATA`.

- CSV ingestion from the configured source directory; current repository source is `data/raw/BASE_DATA.csv`.
- Complete-file SHA-256 is used for source-file version detection.
- `ETL_CONTROL` checks the source filename and file hash against successful processing.
- Bronze writes append; it does not perform record-level MERGE.
- `RECORD_HASH` is a separate row-level fingerprint, not the complete-file hash.
- Final validated source count recorded in `docs/VALIDATION.md`: 228,711.

## Silver

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

- Observation-level tables use `(ID_POLICY, ID_INSURED, PERIOD)`.
- `SILVER_TIME` contains only `PERIOD`, one row per distinct period.
- Policy lifecycle year fields belong to `SILVER_POLICY`.
- Insured lifecycle year fields belong to `SILVER_CUSTOMER`.
- `COST_CLAIMS_YEAR` belongs to `SILVER_FINANCIAL`.
- `SILVER_STAGE` is technical staging, not a ninth business table.
- Oracle MERGE is used; it is not SCD Type 2.

## Gold

Five dimensions and one fact:

```text
DIM_TIME
DIM_CUSTOMER
DIM_POLICY
DIM_PRODUCT
DIM_CHANNEL
FACT_POLICY
```

Grains/business keys defined by DDL:
- `DIM_TIME`: `PERIOD`
- `DIM_CUSTOMER`: `(ID_POLICY, ID_INSURED)`
- `DIM_POLICY`: `ID_POLICY`
- `DIM_PRODUCT`: `(TYPE_PRODUCT, REIMBURSEMENT)`
- `DIM_CHANNEL`: `DISTRIBUTION_CHANNEL`
- `FACT_POLICY`: `(ID_POLICY, ID_INSURED, PERIOD)`

Gold transformation selects the latest observation period for each customer and policy dimension business key; product, channel and time inputs are distinct values. The current Gold loader performs a full refresh. There is no SCD Type 2 implementation and no `FACT_CLAIMS`. `COST_CLAIMS_YEAR` remains a policy-insured-period fact measure.

`GOLD_STAGE` is technical staging only.

## Orchestration

- Python orchestration: `src/orchestration/pipeline.py`.
- Airflow DAG: `dags/insurance_risk_intelligence_pipeline.py`.
- Task dependency: `bronze >> silver >> gold`.
- DAG configuration: `schedule=None`, `catchup=False`, `max_active_runs=1`.
- The DAG is unscheduled/manual by configuration. Refer to validation evidence for the recorded manual run; do not claim a production schedule.

## FastAPI

The repository contains a FastAPI analytics API under `src/api/`. It reads Gold analytics data through the configured API database connection. API security, routes and runtime evidence must be described from the API source and README; do not imply write access to warehouse data.

## Streamlit

The repository contains a six-page dashboard under `src/dashboard/`. It consumes the API through its API client and is not designed as a direct Oracle client. See `docs/DASHBOARD.md`.

## RAG / NL2SQL

RAG, vector database, embeddings, LLM provider integration and NL2SQL are future work, not implemented in the current repository. Do not select or describe a provider/model/vector store as frozen until separately researched and explicitly decided.

## Documentation map

- `docs/01_Business_Documents/`: business objectives, glossary and source dictionary.
- `docs/02_Data_Architecture/`: source system, data model, data flow, naming and Medallion documentation.
- `docs/ARCHITECTURE.md`: concise implemented architecture.
- `docs/ORCHESTRATION.md`: Python/Airflow execution contract.
- `docs/DASHBOARD.md`: Streamlit pages and API consumption.
- `docs/VALIDATION.md`: recorded warehouse and orchestration validation.

When updating documentation, inspect the relevant SQL and Python source first. If implementation evidence does not establish a statement, label it unverified or omit it rather than infer it.
