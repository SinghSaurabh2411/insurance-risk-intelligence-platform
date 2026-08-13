"""
==========================================================
Project : Insurance Risk Intelligence Platform
Module  : Oracle Helper Utility
Author  : Saurabh Singh

Description
-----------
Provides reusable Oracle database helper functions for
the ETL pipeline.

Responsibilities
----------------
1. Test Oracle connectivity
2. Read Oracle tables into Spark DataFrames
3. Write Spark DataFrames to Oracle
4. Execute Oracle SQL statements
5. Execute Oracle MERGE statements

This module contains NO ETL business logic.

Schema-specific credentials are supplied by the caller
through jdbc_properties.

==========================================================
"""

import oracledb

from pyspark.sql import DataFrame, SparkSession

from config.oracle_config import (
    ORACLE_HOST,
    ORACLE_PORT,
    ORACLE_SERVICE,
    JDBC_URL
)

from utils.logger import get_logger


# ==========================================================
# Logger
# ==========================================================

logger = get_logger(
    layer="bronze",
    module_name="oracle_helper"
)


# ==========================================================
# Oracle Connection
# ==========================================================

def get_connection(jdbc_properties: dict):
    """
    Creates and returns an Oracle database connection.

    Parameters
    ----------
    jdbc_properties : dict
        Oracle connection properties containing:
        user
        password
        driver

    Returns
    -------
    oracledb.Connection
    """

    try:

        connection = oracledb.connect(
            user=jdbc_properties["user"],
            password=jdbc_properties["password"],
            host=ORACLE_HOST,
            port=int(ORACLE_PORT),
            service_name=ORACLE_SERVICE
        )

        return connection

    except Exception:

        logger.exception(
            "Failed to establish Oracle connection."
        )

        raise


# ==========================================================
# Test Oracle Connection
# ==========================================================

def test_connection(jdbc_properties: dict) -> bool:
    """
    Tests Oracle database connectivity.

    Parameters
    ----------
    jdbc_properties : dict
        Oracle JDBC properties.

    Returns
    -------
    bool
        True if connection succeeds.
    """

    connection = None

    try:

        connection = get_connection(jdbc_properties)

        logger.info(
            "Oracle connection successful for user: %s",
            jdbc_properties["user"]
        )

        return True

    except Exception:

        logger.exception(
            "Oracle connection test failed."
        )

        raise

    finally:

        if connection is not None:
            connection.close()


# ==========================================================
# Read Oracle Table
# ==========================================================

def read_table(
    spark: SparkSession,
    table_name: str,
    jdbc_properties: dict
) -> DataFrame:
    """
    Reads an Oracle table into a Spark DataFrame.

    Parameters
    ----------
    spark : SparkSession
        Active Spark session.

    table_name : str
        Fully qualified Oracle table name.

        Example:
        DWH_BRONZE.BRONZE_POLICY_DATA

    jdbc_properties : dict
        Oracle JDBC properties.

    Returns
    -------
    DataFrame
        Spark DataFrame containing Oracle table data.
    """

    logger.info(
        "Reading Oracle table: %s",
        table_name
    )

    try:

        dataframe = (
            spark.read
            .jdbc(
                url=JDBC_URL,
                table=table_name,
                properties=jdbc_properties
            )
        )

        logger.info(
            "Successfully created DataFrame from: %s",
            table_name
        )

        return dataframe

    except Exception:

        logger.exception(
            "Failed to read Oracle table: %s",
            table_name
        )

        raise


# ==========================================================
# Write DataFrame to Oracle
# ==========================================================

def write_dataframe(
    dataframe: DataFrame,
    table_name: str,
    jdbc_properties: dict,
    mode: str = "append"
) -> None:
    """
    Writes a Spark DataFrame to an Oracle table.

    Parameters
    ----------
    dataframe : DataFrame
        Spark DataFrame to write.

    table_name : str
        Fully qualified Oracle table name.

    jdbc_properties : dict
        Oracle JDBC properties.

    mode : str
        Spark write mode.

        Default:
        append

    Returns
    -------
    None
    """

    logger.info(
        "Writing DataFrame to Oracle table: %s",
        table_name
    )

    try:

        (
            dataframe.write
            .jdbc(
                url=JDBC_URL,
                table=table_name,
                mode=mode,
                properties=jdbc_properties
            )
        )

        logger.info(
            "Successfully wrote DataFrame to: %s",
            table_name
        )

    except Exception:

        logger.exception(
            "Failed to write DataFrame to: %s",
            table_name
        )

        raise


# ==========================================================
# Execute SQL
# ==========================================================

def execute_sql(
    sql_statement: str,
    jdbc_properties: dict
) -> None:
    """
    Executes an Oracle SQL statement.

    Intended for DDL/DML/control operations.

    Parameters
    ----------
    sql_statement : str
        SQL statement to execute.

    jdbc_properties : dict
        Oracle JDBC properties.

    Returns
    -------
    None
    """

    connection = None
    cursor = None

    try:

        connection = get_connection(jdbc_properties)

        cursor = connection.cursor()

        cursor.execute(sql_statement)

        connection.commit()

        logger.info(
            "Oracle SQL executed successfully."
        )

    except Exception:

        if connection is not None:
            connection.rollback()

        logger.exception(
            "Oracle SQL execution failed."
        )

        raise

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


# ==========================================================
# Execute MERGE
# ==========================================================

def execute_merge(
    merge_sql: str,
    jdbc_properties: dict
) -> None:
    """
    Executes an Oracle MERGE statement.

    MERGE statements are used by the ETL pipeline for
    incremental loading and upsert operations.

    Parameters
    ----------
    merge_sql : str
        Oracle MERGE statement.

    jdbc_properties : dict
        Oracle JDBC properties.

    Returns
    -------
    None
    """

    logger.info(
        "Starting Oracle MERGE."
    )

    execute_sql(
        sql_statement=merge_sql,
        jdbc_properties=jdbc_properties
    )

    logger.info(
        "Oracle MERGE completed successfully."
    )