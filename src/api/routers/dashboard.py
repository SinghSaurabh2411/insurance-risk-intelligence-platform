"""
===============================================================================
Project : Insurance Risk Intelligence Platform
Module  : Dashboard API Routes
Purpose : Expose read-only analytical summary KPIs from the Gold layer.
===============================================================================
"""

from fastapi import APIRouter, HTTPException

from api.database import get_api_connection
from utils.logger import get_logger


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

logger = get_logger(
    layer="api",
    module_name="dashboard",
)


SUMMARY_SQL = """
WITH POLICY_PERIOD_CLAIMS AS (
    SELECT
        ID_POLICY,
        PERIOD,
        MAX(COST_CLAIMS_YEAR) AS COST_CLAIMS_YEAR
    FROM DWH_GOLD.FACT_POLICY
    GROUP BY ID_POLICY, PERIOD
),
CLAIMS_TOTAL AS (
    SELECT
        NVL(SUM(COST_CLAIMS_YEAR), 0) AS TOTAL_CLAIMS_COST
    FROM POLICY_PERIOD_CLAIMS
)
SELECT
    COUNT(DISTINCT F.ID_POLICY) AS TOTAL_POLICIES,
    COUNT(*) AS TOTAL_OBSERVATIONS,
    NVL(SUM(F.PREMIUM), 0) AS TOTAL_PREMIUM,
    C.TOTAL_CLAIMS_COST,
    NVL(AVG(F.PREMIUM), 0) AS AVERAGE_PREMIUM,
    NVL(SUM(F.EXPOSURE_TIME), 0) AS TOTAL_EXPOSURE
FROM DWH_GOLD.FACT_POLICY F
CROSS JOIN CLAIMS_TOTAL C
GROUP BY C.TOTAL_CLAIMS_COST
"""


@router.get("/summary")
def get_dashboard_summary():
    """
    Return high-level insurance portfolio KPIs from Gold FACT_POLICY.
    """

    connection = None

    try:
        connection = get_api_connection()

        with connection.cursor() as cursor:
            cursor.execute(SUMMARY_SQL)
            row = cursor.fetchone()

        if row is None:
            raise RuntimeError("Dashboard summary query returned no result.")

        return {
            "total_policies": int(row[0]),
            "total_observations": int(row[1]),
            "total_premium": float(row[2]),
            "total_claims_cost": float(row[3]),
            "average_premium": float(row[4]),
            "total_exposure": float(row[5]),
        }

    except Exception as exc:
        logger.exception("Dashboard summary query failed.")

        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve dashboard summary.",
        ) from exc

    finally:
        if connection is not None:
            connection.close()
