""" 
==========================================================
Project : Insurance Risk Intelligence Platform
Module  : ETL Control Table Utility
Author  : Saurabh Singh

Description
-----------
Provides reusable functions for interacting with the
DWH_CONTROL.ETL_CONTROL table.

The Python contract in this module is aligned with the
current Oracle ETL_CONTROL DDL.

No business transformation logic should exist here.

==========================================================
"""

from typing import Optional

from config.oracle_config import (
    CONTROL_SCHEMA,
    CONTROL_JDBC_PROPERTIES
)

from utils.oracle_helper import (
    get_connection
)

from utils.logger import get_logger


# ==========================================================
# Logger
# ==========================================================

logger = get_logger(
    layer="bronze",
    module_name="control_table"
)


# ==========================================================
# Control Table
# ==========================================================

CONTROL_TABLE = f"{CONTROL_SCHEMA}.ETL_CONTROL"


# ==========================================================
# Sequence
# ==========================================================

LOAD_ID_SEQUENCE = f"{CONTROL_SCHEMA}.SEQ_LOAD_ID"


# ==========================================================
# Check File Already Processed
# ==========================================================

def is_file_processed(
    source_file: str
) -> bool:
    """
    Checks whether a source file has already been
    successfully processed.
    """

    connection = None
    cursor = None

    sql = f"""
        SELECT COUNT(1)
        FROM {CONTROL_TABLE}
        WHERE SOURCE_FILE = :source_file
          AND LOAD_STATUS = 'SUCCESS'
    """

    try:
        connection = get_connection(
            CONTROL_JDBC_PROPERTIES
        )

        cursor = connection.cursor()

        cursor.execute(
            sql,
            {
                "source_file": source_file
            }
        )

        count = cursor.fetchone()[0]

        processed = count > 0

        logger.info(
            "File '%s' processed status: %s",
            source_file,
            processed
        )

        return processed

    except Exception:
        logger.exception(
            "Failed to check processed status for file: %s",
            source_file
        )
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


# ==========================================================
# Generate LOAD_ID
# ==========================================================

def generate_load_id() -> int:
    """
    Generates a new LOAD_ID using the Oracle sequence.
    """

    connection = None
    cursor = None

    sql = f"""
        SELECT {LOAD_ID_SEQUENCE}.NEXTVAL
        FROM DUAL
    """

    try:
        connection = get_connection(
            CONTROL_JDBC_PROPERTIES
        )

        cursor = connection.cursor()

        cursor.execute(sql)

        load_id = cursor.fetchone()[0]

        logger.info(
            "Generated LOAD_ID: %s",
            load_id
        )

        return load_id

    except Exception:
        logger.exception(
            "Failed to generate LOAD_ID."
        )
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


# ==========================================================
# Register ETL Load
# ==========================================================

def register_load(
    load_id: int,
    layer_name: str,
    pipeline_name: str,
    source_file: str,
    source_file_hash: str,
    source_record_count: int,
    created_by: str
) -> None:
    """
    Registers the beginning of an ETL load.

    SOURCE_FILE_HASH is the SHA-256 checksum of the
    complete raw source file.
    """

    connection = None
    cursor = None

    sql = f"""
        INSERT INTO {CONTROL_TABLE}
        (
            LOAD_ID,
            LAYER_NAME,
            PIPELINE_NAME,
            SOURCE_FILE,
            SOURCE_FILE_HASH,
            SOURCE_RECORD_COUNT,
            LOAD_STATUS,
            START_TIME,
            CREATED_BY
        )
        VALUES
        (
            :load_id,
            :layer_name,
            :pipeline_name,
            :source_file,
            :source_file_hash,
            :source_record_count,
            'STARTED',
            SYSTIMESTAMP,
            :created_by
        )
    """

    try:
        connection = get_connection(
            CONTROL_JDBC_PROPERTIES
        )

        cursor = connection.cursor()

        cursor.execute(
            sql,
            {
                "load_id": load_id,
                "layer_name": layer_name,
                "pipeline_name": pipeline_name,
                "source_file": source_file,
                "source_file_hash": source_file_hash,
                "source_record_count": source_record_count,
                "created_by": created_by
            }
        )

        connection.commit()

        logger.info(
            "Registered ETL load: LOAD_ID=%s, FILE=%s",
            load_id,
            source_file
        )

    except Exception:
        if connection is not None:
            connection.rollback()

        logger.exception(
            "Failed to register ETL load: %s",
            load_id
        )

        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


# ==========================================================
# Update Load Status
# ==========================================================

def update_load_status(
    load_id: int,
    status: str,
    error_message: Optional[str] = None,
    target_record_count: Optional[int] = None
) -> None:
    """
    Updates the status of an ETL load.

    Allowed values are defined by the current Oracle DDL:

        STARTED
        SUCCESS
        FAILED
    """

    allowed_statuses = {
        "STARTED",
        "SUCCESS",
        "FAILED"
    }

    status = status.upper()

    if status not in allowed_statuses:
        raise ValueError(
            f"Invalid ETL status: {status}. "
            f"Allowed values: {allowed_statuses}"
        )

    connection = None
    cursor = None

    if status == "STARTED":
        sql = f"""
            UPDATE {CONTROL_TABLE}
            SET
                LOAD_STATUS = :load_status,
                ERROR_MESSAGE = :error_message
            WHERE LOAD_ID = :load_id
        """
    else:
        sql = f"""
            UPDATE {CONTROL_TABLE}
            SET
                LOAD_STATUS = :load_status,
                TARGET_RECORD_COUNT = :target_record_count,
                END_TIME = SYSTIMESTAMP,
                ERROR_MESSAGE = :error_message
            WHERE LOAD_ID = :load_id
        """

    try:
        connection = get_connection(
            CONTROL_JDBC_PROPERTIES
        )

        cursor = connection.cursor()

        cursor.execute(
            sql,
            {
                "load_status": status,
                "target_record_count": target_record_count,
                "error_message": error_message,
                "load_id": load_id
            }
        )

        connection.commit()

        logger.info(
            "Updated LOAD_ID=%s to status=%s",
            load_id,
            status
        )

    except Exception:
        if connection is not None:
            connection.rollback()

        logger.exception(
            "Failed to update LOAD_ID=%s",
            load_id
        )

        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


# ==========================================================
# Get Latest Load
# ==========================================================

def get_latest_load() -> Optional[dict]:
    """
    Retrieves the latest ETL load from the control table.
    """

    connection = None
    cursor = None

    sql = f"""
        SELECT
            LOAD_ID,
            LAYER_NAME,
            PIPELINE_NAME,
            SOURCE_FILE,
            SOURCE_FILE_HASH,
            SOURCE_RECORD_COUNT,
            TARGET_RECORD_COUNT,
            LOAD_STATUS,
            START_TIME,
            END_TIME,
            ERROR_MESSAGE,
            CREATED_BY
        FROM {CONTROL_TABLE}
        ORDER BY LOAD_ID DESC
        FETCH FIRST 1 ROW ONLY
    """

    try:
        connection = get_connection(
            CONTROL_JDBC_PROPERTIES
        )

        cursor = connection.cursor()

        cursor.execute(sql)

        row = cursor.fetchone()

        if row is None:
            return None

        columns = [
            "LOAD_ID",
            "LAYER_NAME",
            "PIPELINE_NAME",
            "SOURCE_FILE",
            "SOURCE_FILE_HASH",
            "SOURCE_RECORD_COUNT",
            "TARGET_RECORD_COUNT",
            "LOAD_STATUS",
            "START_TIME",
            "END_TIME",
            "ERROR_MESSAGE",
            "CREATED_BY"
        ]

        return dict(
            zip(columns, row)
        )

    except Exception:
        logger.exception(
            "Failed to retrieve latest ETL load."
        )
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()
