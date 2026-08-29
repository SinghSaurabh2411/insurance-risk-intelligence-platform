"""
===============================================================================
Project : Insurance Risk Intelligence Platform
File    : main.py
Purpose : Application entry point
===============================================================================

Description
-----------
Main entry point for the Insurance Risk Intelligence Platform ETL pipeline.

Responsibilities
----------------
1. Create the SparkSession.
2. Start the Bronze ETL pipeline.
3. Handle top-level exceptions.
4. Stop Spark gracefully.

This module does NOT contain:
    - ETL transformation logic
    - Oracle connection logic
    - File discovery logic
    - Validation logic
    - Business logic

Those responsibilities belong to their respective modules.

===============================================================================
"""

import sys

from config.config import PROJECT_NAME

from utils.spark_session import create_spark_session

from utils.logger import get_logger

from bronze.bronze_loader import run_bronze_pipeline


# =============================================================================
# LOGGER
# =============================================================================

logger = get_logger(
    layer="bronze",
    module_name="main",
)


# =============================================================================
# MAIN
# =============================================================================

def main() -> int:
    """
    Application entry point.

    Returns
    -------
    int
        Process exit code.

        0 -> successful execution
        1 -> execution failure
    """

    spark = None

    logger.info(
        "================================================================"
    )

    logger.info(
        "Starting %s",
        PROJECT_NAME,
    )

    try:

        # =====================================================================
        # 1. CREATE SPARK SESSION
        # =====================================================================

        logger.info(
            "Creating SparkSession."
        )

        spark = create_spark_session()

        logger.info(
            "SparkSession created successfully."
        )

        # =====================================================================
        # 2. RUN BRONZE ETL
        # =====================================================================

        logger.info(
            "Starting Bronze ETL pipeline."
        )

        run_bronze_pipeline(
            spark=spark,
        )

        logger.info(
            "Bronze ETL pipeline completed successfully."
        )

        logger.info(
            "Application completed successfully."
        )

        return 0

    except Exception as exception:

        logger.exception(
            "Application execution failed: %s",
            str(exception),
        )

        return 1

    finally:

        # =====================================================================
        # 3. STOP SPARK
        # =====================================================================

        if spark is not None:

            try:

                logger.info(
                    "Stopping SparkSession."
                )

                spark.stop()

                logger.info(
                    "SparkSession stopped successfully."
                )

            except Exception:

                logger.exception(
                    "Error while stopping SparkSession."
                )

        logger.info(
            "================================================================"
        )


# =============================================================================
# SCRIPT ENTRY POINT
# =============================================================================

if __name__ == "__main__":

    exit_code = main()

    sys.exit(exit_code)