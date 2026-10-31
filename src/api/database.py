"""
===============================================================================
Project : Insurance Risk Intelligence Platform
Module  : API Database Connection
Purpose : Provide dedicated read-only Oracle connections for the API.
===============================================================================

The API uses a separate DWH_API database account. It never falls back to the
Gold ETL credentials and does not reuse ETL SQL execution utilities.

Required environment variables:
    API_USER
    API_PASSWORD
    ORACLE_HOST
    ORACLE_PORT
    ORACLE_SERVICE

===============================================================================
"""

import os

import oracledb

from config.oracle_config import (
    ORACLE_HOST,
    ORACLE_PORT,
    ORACLE_SERVICE,
)
from utils.logger import get_logger


logger = get_logger(
    layer="api",
    module_name="database",
)


def get_api_connection():
    """
    Create and return a read-only Oracle connection for API requests.

    The caller owns the returned connection and must close it after use.
    A read-only transaction is started immediately, before any query executes.

    Returns
    -------
    oracledb.Connection

    Raises
    ------
    RuntimeError
        If required API credentials or Oracle connection settings are missing.
    oracledb.Error
        If Oracle connection or read-only transaction initialization fails.
    """

    api_user = os.getenv("API_USER")
    api_password = os.getenv("API_PASSWORD")

    required_settings = {
        "API_USER": api_user,
        "API_PASSWORD": api_password,
        "ORACLE_HOST": ORACLE_HOST,
        "ORACLE_PORT": ORACLE_PORT,
        "ORACLE_SERVICE": ORACLE_SERVICE,
    }

    missing_settings = [
        name
        for name, value in required_settings.items()
        if not value
    ]

    if missing_settings:
        raise RuntimeError(
            "Missing API database configuration: "
            + ", ".join(missing_settings)
        )

    connection = None

    try:
        connection = oracledb.connect(
            user=api_user,
            password=api_password,
            host=ORACLE_HOST,
            port=int(ORACLE_PORT),
            service_name=ORACLE_SERVICE,
        )

        # Must be the first statement in this transaction.
        with connection.cursor() as cursor:
            cursor.execute("SET TRANSACTION READ ONLY")

        logger.info(
            "Read-only Oracle connection established for API user."
        )

        return connection

    except Exception:
        if connection is not None:
            connection.close()

        logger.exception(
            "Failed to establish read-only Oracle API connection."
        )
        raise
