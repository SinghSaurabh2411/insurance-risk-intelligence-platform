"""
===============================================================================
Project : Insurance Risk Intelligence Platform
Module  : Dashboard Customer Routes
Purpose : Expose customer-level portfolio breakdowns.
===============================================================================
"""

from fastapi import APIRouter, Depends, HTTPException

from api.security import require_api_key
from api.models import CustomersResponse, CustomerCohortsResponse

from api.database import get_api_connection
from utils.logger import get_logger


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(require_api_key)],
)

logger = get_logger(
    layer="api",
    module_name="dashboard customer routes",
)


CUSTOMER_SQL = """
SELECT
    C.GENDER,
    COUNT(*) AS TOTAL_OBSERVATIONS,
    COUNT(DISTINCT F.CUSTOMER_KEY) AS TOTAL_CUSTOMER_RECORDS,
    COUNT(DISTINCT F.ID_POLICY) AS TOTAL_POLICIES,
    NVL(SUM(F.PREMIUM), 0) AS TOTAL_PREMIUM,
    NVL(SUM(F.COST_CLAIMS_YEAR), 0) AS TOTAL_CLAIMS_COST,
    NVL(AVG(F.PREMIUM), 0) AS AVERAGE_PREMIUM,
    NVL(SUM(F.EXPOSURE_TIME), 0) AS TOTAL_EXPOSURE
FROM DWH_GOLD.FACT_POLICY F
INNER JOIN DWH_GOLD.DIM_CUSTOMER C
    ON F.CUSTOMER_KEY = C.CUSTOMER_KEY
GROUP BY C.GENDER
ORDER BY C.GENDER
"""


CUSTOMER_COHORT_SQL = """
SELECT
    C.YEAR_EFFECT_INSURED,
    COUNT(*) AS TOTAL_OBSERVATIONS,
    COUNT(DISTINCT F.CUSTOMER_KEY) AS TOTAL_CUSTOMER_RECORDS,
    COUNT(DISTINCT F.ID_POLICY) AS TOTAL_POLICIES,
    NVL(SUM(F.PREMIUM), 0) AS TOTAL_PREMIUM,
    NVL(SUM(F.COST_CLAIMS_YEAR), 0) AS TOTAL_CLAIMS_COST,
    NVL(AVG(F.PREMIUM), 0) AS AVERAGE_PREMIUM,
    NVL(SUM(F.EXPOSURE_TIME), 0) AS TOTAL_EXPOSURE
FROM DWH_GOLD.FACT_POLICY F
INNER JOIN DWH_GOLD.DIM_CUSTOMER C
    ON F.CUSTOMER_KEY = C.CUSTOMER_KEY
GROUP BY C.YEAR_EFFECT_INSURED
ORDER BY C.YEAR_EFFECT_INSURED NULLS LAST
"""


@router.get("/customers", response_model=CustomersResponse)
def get_dashboard_customers():
    """
    Return portfolio KPIs grouped by insured gender.
    """

    connection = None

    try:
        connection = get_api_connection()

        with connection.cursor() as cursor:
            cursor.execute(CUSTOMER_SQL)
            rows = cursor.fetchall()

        customers = [
            {
                "gender": row[0],
                "total_observations": int(row[1]),
                "total_customer_records": int(row[2]),
                "total_policies": int(row[3]),
                "total_premium": float(row[4]),
                "total_claims_cost": float(row[5]),
                "average_premium": float(row[6]),
                "total_exposure": float(row[7]),
            }
            for row in rows
        ]

        return {"customers": customers}

    except Exception as exc:
        logger.exception("Dashboard customer breakdown query failed.")

        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve customer dashboard metrics.",
        ) from exc

    finally:
        if connection is not None:
            connection.close()


@router.get("/customer-cohorts", response_model=CustomerCohortsResponse)
def get_dashboard_customer_cohorts():
    """
    Return portfolio KPIs grouped by insured coverage effective year.
    """

    connection = None

    try:
        connection = get_api_connection()

        with connection.cursor() as cursor:
            cursor.execute(CUSTOMER_COHORT_SQL)
            rows = cursor.fetchall()

        customer_cohorts = [
            {
                "year_effect_insured": (
                    int(row[0]) if row[0] is not None else None
                ),
                "total_observations": int(row[1]),
                "total_customer_records": int(row[2]),
                "total_policies": int(row[3]),
                "total_premium": float(row[4]),
                "total_claims_cost": float(row[5]),
                "average_premium": float(row[6]),
                "total_exposure": float(row[7]),
            }
            for row in rows
        ]

        return {"customer_cohorts": customer_cohorts}

    except Exception as exc:
        logger.exception("Dashboard customer cohort query failed.")

        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve customer cohort metrics.",
        ) from exc

    finally:
        if connection is not None:
            connection.close()
