"""
===============================================================================
Project : Insurance Risk Intelligence Platform
Module  : FastAPI Application
Purpose : API entry point and application health endpoints.
===============================================================================
"""

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.models import HealthResponse, DatabaseHealthResponse
from api.security import get_cors_origins, require_api_key

from api.database import get_api_connection
from utils.logger import get_logger
from api.routers.dashboard import router as dashboard_router
from api.routers.yearly import router as yearly_router
from api.routers.products import router as products_router
from api.routers.channels import router as channels_router
from api.routers.policies import router as policies_router
from api.routers.customers import router as customers_router


logger = get_logger(
    layer="api",
    module_name="main",
)


app = FastAPI(
    title="Insurance Risk Intelligence API",
    description="Read-only analytical API for the Insurance Risk Intelligence Platform.",
    version="1.0.0",
)

cors_origins = get_cors_origins()
if cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=["X-API-Key", "Content-Type"],
    )


app.include_router(dashboard_router)
app.include_router(yearly_router)
app.include_router(products_router)
app.include_router(channels_router)
app.include_router(policies_router)
app.include_router(customers_router)


@app.get("/health", tags=["Health"], response_model=HealthResponse)
def health_check():
    """
    Check whether the API application is running.
    """
    return {
        "status": "healthy",
        "application": "Insurance Risk Intelligence API",
    }


@app.get("/health/db", tags=["Health"], response_model=DatabaseHealthResponse, dependencies=[Depends(require_api_key)])
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
