# Orchestration

## Purpose

Orchestration coordinates the implemented Bronze -> Silver -> Gold pipeline. It does not move transformation, DQ, MERGE, or Gold dimensional logic into a new layer.

## Execution contract

```text
BRONZE
   |
   | success
   v
SILVER
   |
   | success
   v
GOLD
```

A stage exception fails the pipeline and prevents downstream stages from executing.

## Local/manual execution

`src/main.py` is the local entry point and delegates the end-to-end sequence to `src/orchestration/pipeline.py`. The orchestration module can reuse an existing Spark session or create and own one.

## Airflow DAG

The repository contains `dags/insurance_risk_intelligence_pipeline.py`. It defines three Python tasks with dependency:

```text
bronze >> silver >> gold
```

Each task creates its own Spark session, invokes the existing layer loader, and stops its Spark session in a `finally` block.

The DAG uses:
- `schedule=None` (no automatic schedule configured)
- `catchup=False`
- `max_active_runs=1`

The configuration makes the DAG manually triggerable/unscheduled and prevents overlapping DAG runs. No production schedule is claimed.

## Failure behavior

- Bronze failure -> Silver and Gold do not run.
- Silver failure -> Gold does not run.
- Gold failure -> DAG run fails.
- Successful completion -> all three tasks succeed.

The orchestrator delegates to existing layer controls:
- Bronze file/hash idempotency.
- Silver DQ and Oracle MERGE/upsert.
- Gold full refresh.

## Runtime evidence boundary

The repository contains the DAG implementation. Runtime execution claims must be based on an actual Airflow run record or user-provided execution evidence. The project validation record documents a successful manual DAG run; this document does not claim a production deployment or scheduled operation.

## Operational prerequisites

Production operation would require explicit decisions and validation for deployment, Oracle/JDBC/Spark runtime configuration, secrets management, monitoring/alerting, retries, backfills and scheduling. These are not added to the current DAG by this documentation update.

## Design boundary

Do not infer production readiness from the presence of a DAG file. The current DAG implements stage sequencing and failure propagation with no automatic schedule.
