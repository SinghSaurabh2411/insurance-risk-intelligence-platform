"""
===============================================================================
Project : Insurance Risk Intelligence Platform
File    : bronze_loader.py
Purpose : Bronze layer ETL orchestration
===============================================================================

Responsibilities
----------------
This module orchestrates the complete Bronze ingestion process.

Flow
----
1. Discover unprocessed source files
2. Generate LOAD_ID
3. Register ETL load as RUNNING
4. Read source CSV
5. Validate source data
6. Transform source data
7. Generate audit columns and RECORD_HASH
8. Write data to DWH_BRONZE.BRONZE_POLICY_DATA
9. Update ETL_CONTROL as SUCCESS
10. Update ETL_CONTROL as FAILED if an exception occurs

This module does NOT contain:
    - Oracle credentials
    - Spark configuration
    - Transformation logic
    - Hash-generation logic
    - File-discovery logic
    - Control-table SQL

Those responsibilities belong to their respective modules.

===============================================================================
"""

from pathlib import Path
from typing import Optional

from pyspark.sql import DataFrame, SparkSession

from config.config import (
    BRONZE_SOURCE_DIRECTORY,
    BRONZE_POLICY_TABLE_FQN,
    BRONZE_WRITE_MODE,
    CSV_DELIMITER,
    CSV_HAS_HEADER,
    STATUS_RUNNING,
    STATUS_SUCCESS,
    STATUS_FAILED,
    ETL_CREATED_BY,
)

from config.oracle_config import (
    JDBC_URL,
    BRONZE_PROPERTIES,
)

from bronze.bronze_validator import (
    validate_bronze_source,
)

from bronze.bronze_transform import (
    transform_to_bronze,
)

from utils.file_handler import (
    get_unprocessed_files,
)

from utils.control_table import (
    generate_load_id,
    register_load,
    update_load_status,
)

from utils.logger import (
    get_logger,
)


# =============================================================================
# LOGGER
# =============================================================================

logger = get_logger(
    layer="bronze",
    module_name="bronze_loader",
)


# =============================================================================
# READ SOURCE FILE
# =============================================================================

def read_source_file(
    spark: SparkSession,
    source_file: Path,
) -> DataFrame:
    """
    Reads a source CSV file into a Spark DataFrame.

    Source data is intentionally read as STRING values.

    This allows bronze_transform.py to explicitly handle:

        STRING -> DATE
        STRING -> NUMBER

    rather than relying on Spark schema inference.

    Parameters
    ----------
    spark : SparkSession
        Active Spark session.

    source_file : Path
        Source CSV file.

    Returns
    -------
    DataFrame
        Raw source DataFrame.
    """

    logger.info(
        "Reading source file: %s",
        source_file.name,
    )

    dataframe = (
        spark.read
        .option(
            "header",
            str(CSV_HAS_HEADER).lower(),
        )
        .option(
            "delimiter",
            CSV_DELIMITER,
        )
        .option(
            "inferSchema",
            "false",
        )
        .option(
            "mode",
            "FAILFAST",
        )
        .csv(str(source_file))
    )

    logger.info(
        "Successfully read source file: %s",
        source_file.name,
    )

    return dataframe


# =============================================================================
# WRITE BRONZE DATA
# =============================================================================

def write_bronze_data(
    dataframe: DataFrame,
) -> None:
    """
    Writes the transformed DataFrame to the Bronze Oracle
    table through JDBC.

    Target
    ------
    DWH_BRONZE.BRONZE_POLICY_DATA

    Parameters
    ----------
    dataframe : DataFrame
        Bronze-ready DataFrame.

    Returns
    -------
    None
    """

    logger.info(
        "Writing Bronze data to: %s",
        BRONZE_POLICY_TABLE_FQN,
    )

    (
        dataframe.write
        .format("jdbc")
        .option(
            "url",
            JDBC_URL,
        )
        .option(
            "dbtable",
            BRONZE_POLICY_TABLE_FQN,
        )
        .option(
            "user",
            BRONZE_PROPERTIES["user"],
        )
        .option(
            "password",
            BRONZE_PROPERTIES["password"],
        )
        .option(
            "driver",
            BRONZE_PROPERTIES["driver"],
        )
        .mode(
            BRONZE_WRITE_MODE,
        )
        .save()
    )

    logger.info(
        "Bronze data successfully written to: %s",
        BRONZE_POLICY_TABLE_FQN,
    )


# =============================================================================
# PROCESS SINGLE FILE
# =============================================================================

def process_file(
    spark: SparkSession,
    source_file: Path,
) -> bool:
    """
    Processes one source file through the complete Bronze ETL.

    Parameters
    ----------
    spark : SparkSession
        Active Spark session.

    source_file : Path
        Source CSV file.

    Returns
    -------
    bool
        True  -> successful processing
        False -> failed processing
    """

    source_file_name = source_file.name

    load_id: Optional[int] = None

    logger.info(
        "================================================================"
    )

    logger.info(
        "Starting Bronze processing | file=%s",
        source_file_name,
    )

    try:

        # =====================================================================
        # 1. GENERATE LOAD_ID
        # =====================================================================

        load_id = generate_load_id()

        logger.info(
            "Generated LOAD_ID=%s | file=%s",
            load_id,
            source_file_name,
        )

        # =====================================================================
        # 2. REGISTER LOAD
        # =====================================================================

        register_load(
            load_id=load_id,
            source_file=source_file_name,
            etl_created_by=ETL_CREATED_BY,
        )

        logger.info(
            "ETL load registered as %s | LOAD_ID=%s",
            STATUS_RUNNING,
            load_id,
        )

        # =====================================================================
        # 3. READ SOURCE FILE
        # =====================================================================

        dataframe = read_source_file(
            spark=spark,
            source_file=source_file,
        )

        # =====================================================================
        # 4. VALIDATE SOURCE
        # =====================================================================

        validate_bronze_source(
            dataframe=dataframe,
        )

        logger.info(
            "Bronze validation successful | LOAD_ID=%s",
            load_id,
        )

        # =====================================================================
        # 5. TRANSFORM SOURCE
        # =====================================================================

        bronze_dataframe = transform_to_bronze(
            dataframe=dataframe,
            load_id=load_id,
            source_file=source_file_name,
            etl_created_by=ETL_CREATED_BY,
        )

        logger.info(
            "Bronze transformation successful | LOAD_ID=%s",
            load_id,
        )

        # =====================================================================
        # 6. WRITE TO ORACLE BRONZE
        # =====================================================================

        write_bronze_data(
            dataframe=bronze_dataframe,
        )

        # =====================================================================
        # 7. MARK LOAD SUCCESSFUL
        # =====================================================================

        update_load_status(
            load_id=load_id,
            status=STATUS_SUCCESS,
        )

        logger.info(
            "Bronze load completed successfully | "
            "LOAD_ID=%s | file=%s",
            load_id,
            source_file_name,
        )

        return True

    except Exception as exception:

        # =====================================================================
        # LOG FAILURE
        # =====================================================================

        logger.exception(
            "Bronze processing failed | file=%s | error=%s",
            source_file_name,
            str(exception),
        )

        # =====================================================================
        # UPDATE CONTROL TABLE
        # =====================================================================

        if load_id is not None:

            try:

                update_load_status(
                    load_id=load_id,
                    status=STATUS_FAILED,
                    error_message=str(exception),
                )

                logger.info(
                    "ETL load marked as %s | LOAD_ID=%s",
                    STATUS_FAILED,
                    load_id,
                )

            except Exception:

                logger.exception(
                    "Unable to update ETL_CONTROL after "
                    "Bronze failure | LOAD_ID=%s",
                    load_id,
                )

        return False


# =============================================================================
# RUN BRONZE PIPELINE
# =============================================================================

def run_bronze_pipeline(
    spark: SparkSession,
) -> None:
    """
    Executes the Bronze ETL pipeline.

    Parameters
    ----------
    spark : SparkSession
        Active Spark session.

    Returns
    -------
    None

    Raises
    ------
    RuntimeError
        If one or more source files fail processing.
    """

    logger.info(
        "================================================================"
    )

    logger.info(
        "Starting Bronze ETL pipeline."
    )

    logger.info(
        "Source directory: %s",
        BRONZE_SOURCE_DIRECTORY,
    )

    # =========================================================================
    # 1. DISCOVER UNPROCESSED FILES
    # =========================================================================

    source_files = get_unprocessed_files(
        BRONZE_SOURCE_DIRECTORY,
    )

    # =========================================================================
    # 2. NOTHING TO PROCESS
    # =========================================================================

    if not source_files:

        logger.info(
            "No unprocessed source files found."
        )

        logger.info(
            "Bronze ETL completed. Nothing to process."
        )

        return

    logger.info(
        "Found %d unprocessed source file(s).",
        len(source_files),
    )

    # =========================================================================
    # 3. PROCESS FILES
    # =========================================================================

    failed_files = []

    for source_file in source_files:

        success = process_file(
            spark=spark,
            source_file=source_file,
        )

        if not success:

            failed_files.append(
                source_file.name
            )

    # =========================================================================
    # 4. FINAL PIPELINE STATUS
    # =========================================================================

    if failed_files:

        logger.error(
            "Bronze ETL completed with failures."
        )

        logger.error(
            "Failed files: %s",
            failed_files,
        )

        raise RuntimeError(
            "Bronze ETL failed for one or more files: "
            f"{failed_files}"
        )

    logger.info(
        "Bronze ETL pipeline completed successfully."
    )

    logger.info(
        "================================================================"
    )


# =============================================================================
# END OF FILE
# =============================================================================