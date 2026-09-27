"""Thin orchestration layer for the frozen Bronze -> Silver -> Gold pipeline."""

import logging
from typing import Callable, Optional

from pyspark.sql import SparkSession

from utils.spark_session import create_spark_session
from bronze.bronze_loader import run_bronze_pipeline
from silver.silver_loader import run_silver_pipeline
from gold.gold_loader import run_gold_pipeline

logger = logging.getLogger("application.orchestration")


def _run_stage(stage_name: str, stage_runner: Callable[[SparkSession], None], spark: SparkSession) -> None:
    """Run one existing ETL stage and fail immediately on exception."""
    logger.info("Starting orchestration stage: %s", stage_name)
    stage_runner(spark=spark)
    logger.info("Completed orchestration stage: %s", stage_name)


def run_pipeline(spark: Optional[SparkSession] = None) -> None:
    """Run the validated Bronze -> Silver -> Gold sequence."""
    owns_spark = spark is None
    active_spark = spark or create_spark_session()

    try:
        logger.info("Starting end-to-end Insurance Risk Intelligence pipeline.")
        _run_stage("BRONZE", run_bronze_pipeline, active_spark)
        _run_stage("SILVER", run_silver_pipeline, active_spark)
        _run_stage("GOLD", run_gold_pipeline, active_spark)
        logger.info("End-to-end pipeline completed successfully.")
    except Exception:
        logger.exception("End-to-end pipeline failed. Downstream stages were not executed.")
        raise
    finally:
        if owns_spark:
            active_spark.stop()
