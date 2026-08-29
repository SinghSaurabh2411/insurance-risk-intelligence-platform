"""
===============================================================================
Project : Insurance Risk Intelligence Platform
Module  : Spark Session Utility
Author  : Saurabh Singh

Description
-----------
Creates and manages the SparkSession used across the ETL pipeline.

Responsibilities
----------------
1. Create SparkSession
2. Configure Spark
3. Configure Oracle JDBC driver
4. Return SparkSession
5. Gracefully stop SparkSession

This module contains Spark-specific configuration.

It does NOT contain:
    - Oracle credentials
    - Project-wide constants
    - Logging configuration
    - ETL business logic

===============================================================================
"""

from pathlib import Path

from pyspark.sql import SparkSession

from utils.logger import get_logger


# =============================================================================
# LOGGER
# =============================================================================

logger = get_logger(
    layer="bronze",
    module_name="spark_session",
)


# =============================================================================
# SPARK CONFIGURATION
# =============================================================================

SPARK_APP_NAME = (
    "Insurance Risk Intelligence Platform"
)

SPARK_MASTER = "local[*]"

SHUFFLE_PARTITIONS = "8"

SPARK_TIMEZONE = "UTC"

SPARK_ADAPTIVE_ENABLED = "true"

SPARK_ARROW_ENABLED = "true"


# =============================================================================
# SPARK SESSION STATE
# =============================================================================

_spark = None


# =============================================================================
# CREATE SPARK SESSION
# =============================================================================

def create_spark_session() -> SparkSession:
    """
    Creates and returns a SparkSession.

    Returns
    -------
    SparkSession
        Active SparkSession.
    """

    global _spark

    # -------------------------------------------------------------------------
    # Return existing session
    # -------------------------------------------------------------------------

    if _spark is not None:

        logger.info(
            "Existing Spark Session returned."
        )

        return _spark

    logger.info(
        "Creating Spark Session..."
    )

    # -------------------------------------------------------------------------
    # Project Root
    # -------------------------------------------------------------------------

    project_root = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    # -------------------------------------------------------------------------
    # Log4j2 Configuration
    # -------------------------------------------------------------------------

    log4j_config = (
            project_root
            / "log4j2.properties"
    )

    if not log4j_config.exists():
        raise FileNotFoundError(
            "Log4j2 configuration file not found: "
            f"{log4j_config}"
        )

    logger.info(
        "Log4j2 configuration found: %s",
        log4j_config,
    )


    # -------------------------------------------------------------------------
    # Oracle JDBC Driver
    # -------------------------------------------------------------------------

    jdbc_jar = (
        project_root
        / "drivers"
        / "ojdbc8.jar"
    )

    # -------------------------------------------------------------------------
    # Verify JDBC Driver
    # -------------------------------------------------------------------------

    if not jdbc_jar.exists():

        raise FileNotFoundError(
            "Oracle JDBC driver not found: "
            f"{jdbc_jar}"
        )

    logger.info(
        "Oracle JDBC driver found: %s",
        jdbc_jar,
    )

    # -------------------------------------------------------------------------
    # Spark Warehouse
    # -------------------------------------------------------------------------

    warehouse_dir = (
        project_root
        / "spark-warehouse"
    )

    warehouse_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -------------------------------------------------------------------------
    # Create Spark Session
    # -------------------------------------------------------------------------

    _spark = (

        SparkSession.builder

        .appName(
            SPARK_APP_NAME
        )

        .master(
            SPARK_MASTER
        )

        # ---------------------------------------------------------------------
        # Oracle JDBC
        # ---------------------------------------------------------------------

        .config(
            "spark.jars",
            str(jdbc_jar),
        )

        # ---------------------------------------------------------------------
        # Spark SQL
        # ---------------------------------------------------------------------

        .config(
            "spark.sql.shuffle.partitions",
            SHUFFLE_PARTITIONS,
        )

        .config(
            "spark.sql.warehouse.dir",
            str(warehouse_dir),
        )

        # ---------------------------------------------------------------------
        # Time Zone
        # ---------------------------------------------------------------------

        .config(
            "spark.sql.session.timeZone",
            SPARK_TIMEZONE,
        )

        # ---------------------------------------------------------------------
        # Adaptive Query Execution
        # ---------------------------------------------------------------------

        .config(
            "spark.sql.adaptive.enabled",
            SPARK_ADAPTIVE_ENABLED,
        )

        # ---------------------------------------------------------------------
        # Arrow
        # ---------------------------------------------------------------------

        .config(
            "spark.sql.execution.arrow.pyspark.enabled",
            SPARK_ARROW_ENABLED,
        )

        .config(
            "spark.driver.extraJavaOptions",
            f"-Dlog4j.configurationFile=file:///{log4j_config.as_posix()}",
        )

        .getOrCreate()
    )

    # 👇 Add this line immediately after session creation
    _spark.sparkContext.setLogLevel("ERROR")

    # -------------------------------------------------------------------------
    # Spark Log Level
    # -------------------------------------------------------------------------

    # _spark.sparkContext.setLogLevel(
    #     "WARN"
    # )

    logger.info(
        "Spark Version : %s",
        _spark.version,
    )

    logger.info(
        "Spark Master : %s",
        SPARK_MASTER,
    )

    logger.info(
        "Spark Session Created Successfully."
    )

    return _spark


# =============================================================================
# GET SPARK SESSION
# =============================================================================

def get_spark() -> SparkSession:
    """
    Returns the singleton SparkSession.

    Returns
    -------
    SparkSession
        Active SparkSession.
    """

    global _spark

    if _spark is None:

        _spark = create_spark_session()

    return _spark


# =============================================================================
# STOP SPARK SESSION
# =============================================================================

def stop_spark() -> None:
    """
    Stops the active SparkSession.
    """

    global _spark

    if _spark is not None:

        logger.info(
            "Stopping Spark Session..."
        )

        _spark.stop()

        _spark = None

        logger.info(
            "Spark Session Stopped."
        )


# =============================================================================
# END OF FILE
# =============================================================================