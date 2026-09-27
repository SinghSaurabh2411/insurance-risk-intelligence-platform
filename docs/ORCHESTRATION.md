# Orchestration

## Purpose

Orchestration coordinates the already-frozen Bronze -> Silver -> Gold implementation. It does not move transformation, DQ, MERGE, or Gold dimensional logic into a new layer.

## Execution contract

    BRONZE
       |
       | success
       v
    SILVER
       |
       | success
       v
    GOLD

A stage exception fails the pipeline and prevents downstream stages from executing.

## Local/manual execution

src/main.py remains the local entry point and delegates the end-to-end sequence to:

    src/orchestration/pipeline.py

The orchestration module can reuse an existing Spark session or create and own one.

## Airflow

The repository contains:

    dags/insurance_risk_intelligence_pipeline.py

The DAG contains three Python tasks:

    bronze >> silver >> gold

Each task creates its own Spark session, invokes the existing layer loader, and stops its Spark session in finally.

The DAG intentionally uses schedule=None and catchup=False. No production schedule has been frozen, so scheduling is left to a future operational decision.

max_active_runs=1 prevents overlapping end-to-end runs.

## Failure behavior

- Bronze failure -> Silver and Gold do not run.
- Silver failure -> Gold does not run.
- Gold failure -> DAG run fails.
- Successful completion -> all three tasks succeed.

Existing layer-level controls remain authoritative:
- Bronze file/hash idempotency
- Silver DQ + Oracle MERGE/upsert
- Gold full refresh

The orchestrator does not duplicate those controls.

## Operational prerequisites

Airflow deployment/runtime is not yet validated in the current local environment. The DAG is repository implementation, not evidence of an executed Airflow run.

A future operationalization step should provide Airflow installation/deployment, Oracle/JDBC/Spark runtime configuration, secrets management, and an explicit production schedule.

## Design boundary

Do not add retries, scheduling policy, alerting, backfills, or parallel branches until operational requirements are explicitly defined. The current DAG implements only deterministic stage sequencing and failure propagation.
