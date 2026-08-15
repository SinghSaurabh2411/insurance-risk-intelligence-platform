"""
==========================================================
Project : Insurance Risk Intelligence Platform
Module  : ETL Control Table Utility
Author  : Saurabh Singh

Description
-----------
Provides reusable functions for interacting with the
DWH_CONTROL.ETL_CONTROL table.

Responsibilities
----------------
1. Check whether a source file was already processed.
2. Register a new ETL load.
3. Update the status of an ETL load.
4. Retrieve the latest load information.
5. Generate LOAD_ID using the Oracle sequence.

The control table is responsible for ETL execution tracking.

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

    Parameters
    ----------
    source_file : str
        Source file name.

    Returns
    -------
    bool
        True  -> file already successfully processed
        False -> file has not been successfully processed
    """

    connection = None
    cursor = None

    sql = f"""
        SELECT COUNT(1)
        FROM {CONTROL_TABLE}
        WHERE SOURCE_FILE = :source_file
          AND STATUS = 'SUCCESS'
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

    Returns
    -------
    int
        Newly generated LOAD_ID.
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
    source_file: str,
    etl_created_by: str
) -> None:
    """
    Registers the beginning of an ETL load.

    Parameters
    ----------
    load_id : int
        Unique ETL load ID.

    source_file : str
        Source file being processed.

    etl_created_by : str
        Name of the ETL process initiating the load.

    Returns
    -------
    None
    """

    connection = None
    cursor = None

    sql = f"""
        INSERT INTO {CONTROL_TABLE}
        (
            LOAD_ID,
            SOURCE_FILE,
            LOAD_TIMESTAMP,
            STATUS,
            ETL_CREATED_BY
        )
        VALUES
        (
            :load_id,
            :source_file,
            SYSTIMESTAMP,
            'RUNNING',
            :etl_created_by
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
                "source_file": source_file,
                "etl_created_by": etl_created_by
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
    error_message: Optional[str] = None
) -> None:
    """
    Updates the status of an ETL load.

    Parameters
    ----------
    load_id : int
        ETL load ID.

    status : str
        Expected values:

        RUNNING
        SUCCESS
        FAILED

    error_message : Optional[str]
        Error details when the load fails.

    Returns
    -------
    None
    """

    allowed_statuses = {
        "RUNNING",
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

    sql = f"""
        UPDATE {CONTROL_TABLE}
        SET
            STATUS = :status,
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
                "status": status,
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

    Returns
    -------
    Optional[dict]
        Latest load information or None if no load exists.
    """

    connection = None
    cursor = None

    sql = f"""
        SELECT
            LOAD_ID,
            SOURCE_FILE,
            LOAD_TIMESTAMP,
            STATUS,
            ETL_CREATED_BY,
            ERROR_MESSAGE
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
            "SOURCE_FILE",
            "LOAD_TIMESTAMP",
            "STATUS",
            "ETL_CREATED_BY",
            "ERROR_MESSAGE"
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