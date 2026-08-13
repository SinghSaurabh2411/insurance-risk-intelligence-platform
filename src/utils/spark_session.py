"""
==========================================================
Project : Insurance Risk Intelligence Platform
Module  : Spark Session Utility
Author  : Saurabh Singh

Description
-----------
Creates and manages a singleton SparkSession used across
the ETL pipeline.

Responsibilities
----------------
1. Create Spark Session
2. Configure Spark SQL
3. Configure Oracle JDBC
4. Return singleton Spark Session
5. Gracefully stop Spark Session

==========================================================
"""

from pathlib import Path

from pyspark.sql import SparkSession

from config.config import (
    APP_NAME,
    SPARK_MASTER,
    SHUFFLE_PARTITIONS,
    WAREHOUSE_DIR
)

from utils.logger import get_logger


# ==========================================================
# Logger
# ==========================================================

logger = get_logger(
    layer="bronze",
    module_name="spark_session"
)

# ==========================================================
# Singleton Spark Session
# ==========================================================

_spark = None


# ==========================================================
# Create Spark Session
# ==========================================================

def create_spark_session() -> SparkSession:
    """
    Creates a SparkSession.

    Returns
    -------
    SparkSession
    """

    logger.info("Creating Spark Session...")

    project_root = Path(__file__).resolve().parents[2]

    jdbc_jar = project_root / "jars" / "ojdbc8.jar"

    spark = (

        SparkSession.builder

        .appName(APP_NAME)

        .master(SPARK_MASTER)

        # ----------------------------------------------
        # JDBC Driver
        # ----------------------------------------------

        .config(
            "spark.jars",
            str(jdbc_jar)
        )

        # ----------------------------------------------
        # Spark SQL
        # ----------------------------------------------

        .config(
            "spark.sql.shuffle.partitions",
            SHUFFLE_PARTITIONS
        )

        .config(
            "spark.sql.warehouse.dir",
            WAREHOUSE_DIR
        )

        .config(
            "spark.sql.session.timeZone",
            "UTC"
        )

        .config(
            "spark.sql.adaptive.enabled",
            "true"
        )

        .config(
            "spark.sql.execution.arrow.pyspark.enabled",
            "true"
        )

        .getOrCreate()

    )

    spark.sparkContext.setLogLevel("WARN")

    logger.info("Spark Version : %s", spark.version)

    logger.info("Spark Session Created Successfully.")

    return spark


# ==========================================================
# Get Spark Session
# ==========================================================

def get_spark() -> SparkSession:
    """
    Returns singleton SparkSession.

    Returns
    -------
    SparkSession
    """

    global _spark

    if _spark is None:

        _spark = create_spark_session()

    return _spark


# ==========================================================
# Stop Spark Session
# ==========================================================

def stop_spark() -> None:
    """
    Stops the Spark Session.
    """

    global _spark

    if _spark is not None:

        logger.info("Stopping Spark Session...")

        _spark.stop()

        _spark = None

        logger.info("Spark Session Stopped.")