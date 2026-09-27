"""Airflow DAG for the Insurance Risk Intelligence Platform."""

from pathlib import Path
import sys

from airflow import DAG
from airflow.operators.python import PythonOperator
from pendulum import datetime

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPOSITORY_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from orchestration.pipeline import _run_stage
from utils.spark_session import create_spark_session
from bronze.bronze_loader import run_bronze_pipeline
from silver.silver_loader import run_silver_pipeline
from gold.gold_loader import run_gold_pipeline


def _run_bronze() -> None:
    spark = create_spark_session()
    try:
        _run_stage("BRONZE", run_bronze_pipeline, spark)
    finally:
        spark.stop()


def _run_silver() -> None:
    spark = create_spark_session()
    try:
        _run_stage("SILVER", run_silver_pipeline, spark)
    finally:
        spark.stop()


def _run_gold() -> None:
    spark = create_spark_session()
    try:
        _run_stage("GOLD", run_gold_pipeline, spark)
    finally:
        spark.stop()


with DAG(
    dag_id="insurance_risk_intelligence_pipeline",
    description="Bronze -> Silver -> Gold insurance risk intelligence pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["insurance", "data-engineering", "bronze", "silver", "gold"],
) as dag:
    bronze = PythonOperator(
        task_id="bronze",
        python_callable=_run_bronze,
    )

    silver = PythonOperator(
        task_id="silver",
        python_callable=_run_silver,
    )

    gold = PythonOperator(
        task_id="gold",
        python_callable=_run_gold,
    )

    bronze >> silver >> gold
