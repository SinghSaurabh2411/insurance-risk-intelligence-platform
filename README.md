# Insurance Risk Intelligence Platform

Portfolio-grade insurance data-engineering and analytics platform using PySpark and Oracle.

## Current status

The core warehouse pipeline is **implemented and validated end to end**:

```text
SOURCE CSV -> BRONZE -> SILVER -> GOLD
```

| Layer | Status |
|---|---|
| Bronze | Implemented, execution validated, frozen |
| Silver | Implemented, DQ/reconciliation/rerun validated, frozen |
| Gold | Implemented, DQ/reconciliation/FK validation completed, frozen |
| Orchestration | Implemented, runtime validation pending |
| Airflow DAG | Implemented, runtime validation pending |
| FastAPI | Planned |
| Streamlit | Planned |
| GenAI / RAG / LLM | Planned |

## Frozen business grain

```text
(ID_POLICY, ID_INSURED, PERIOD)
```

## Bronze

Bronze uses file-level SHA-256 detection, append loading, complete source/business-column `RECORD_HASH`, and `ETL_CONTROL`. It does not perform record-level MERGE.

Final validated row count: **228,711**.

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

Plus technical `DWH_SILVER.SILVER_STAGE`.

Silver uses Oracle MERGE/upsert at the frozen business grain and is not SCD2.

## Gold

Frozen star schema:

```text
DIM_TIME
DIM_CUSTOMER
DIM_POLICY
DIM_PRODUCT
DIM_CHANNEL
FACT_POLICY
```

There is intentionally **no `FACT_CLAIMS`** because the source has no claim-level business entity. `cost_claims_year` remains a policy-period financial measure.

Validated Gold counts:

```text
FACT_POLICY     228,711
DIM_CUSTOMER    100,453
DIM_POLICY       45,162
DIM_PRODUCT           5
DIM_CHANNEL           3
DIM_TIME              3
```

Gold fact grain is `(ID_POLICY, ID_INSURED, PERIOD)`. Dimension business-key duplicates, invalid fact foreign keys, Silver↔Gold grain mismatches, and fact key nulls all validated at zero.

Measure reconciliation completed with only tiny numeric precision differences for Premium and Exposure.

## Documentation

- `Insurance_Risk_Intelligence_Project_Handoff_REVISED.md` — frozen project state
- `docs/ARCHITECTURE.md` — current warehouse architecture and grains
- `docs/VALIDATION.md` — validated execution evidence
- `Database/21_GOLD_DQ_CHECKS.sql` — consolidated Gold validation SQL

## Local execution

```powershell
$env:PYTHONPATH="$PWD\src"
python -m src.main
```

Credentials and local JDBC drivers remain outside Git.

## Orchestration

The repository now provides a thin orchestration layer in `src/orchestration/pipeline.py` and an Airflow DAG in `dags/insurance_risk_intelligence_pipeline.py`.

The execution contract is:

```text
BRONZE -> SILVER -> GOLD
```

The application entry point delegates to the orchestrator. Stage failures stop downstream execution. The Airflow DAG is intentionally unscheduled (`schedule=None`) until an operational schedule is explicitly defined.

Airflow runtime execution is not yet validated.

## Next phase

The data-engineering foundation and orchestration implementation are complete. Next:

```text
Airflow/runtime validation
    ->
API / analytics interfaces
    ->
GenAI / RAG capabilities
```

Do not redesign frozen Bronze, Silver, or Gold layers unless a concrete implementation defect or explicit business requirement requires it.
