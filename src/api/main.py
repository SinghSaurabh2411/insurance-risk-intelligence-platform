"""
===============================================================================
Project : Insurance Risk Intelligence Platform
Module  : FastAPI Application
Purpose : API entry point and application health endpoints.
===============================================================================
"""

from fastapi import FastAPI, HTTPException

from api.database import get_api_connection
from utils.logger import get_logger


logger = get_logger(
    layer="api",
    module_name="main",
)


app = FastAPI(
    title="Insurance Risk Intelligence API",
    description="Read-only analytical API for the Insurance Risk Intelligence Platform.",
    version="1.0.0",
)


@app.get("/health", tags=["Health"])
def health_check():
    """
    Check whether the API application is running.
    """
    return {
        "status": "healthy",
        "application": "Insurance Risk Intelligence API",
    }


@app.get("/health/db", tags=["Health"])
def database_health_check():
    """
    Verify connectivity to Oracle using the dedicated DWH_API account.
    """
    connection = None

    try:
        connection = get_api_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM DUAL")
            result = cursor.fetchone()

        if result is None or result[0] != 1:
            raise RuntimeError("Unexpected database health-check result.")

        return {
            "status": "healthy",
            "database": "Oracle",
            "connection": "successful",
        }

    except Exception as exc:
        logger.exception("Oracle database health check failed.")

        raise HTTPException(
            status_code=503,
            detail="Oracle database is unavailable.",
        ) from exc

    finally:
        if connection is not None:
            connection.close()
