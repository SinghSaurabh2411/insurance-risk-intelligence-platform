"""
===============================================================================
Project : Insurance Risk Intelligence Platform
Module  : Dashboard Yearly Routes
Purpose : Expose yearly portfolio KPIs.
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
    module_name="dashboard yearly routes",
)


YEARLY_SQL = """
SELECT
    T.PERIOD,
    COUNT(*) AS TOTAL_OBSERVATIONS,
    COUNT(DISTINCT F.ID_POLICY) AS TOTAL_POLICIES,
    NVL(SUM(F.PREMIUM), 0) AS TOTAL_PREMIUM,
    NVL(SUM(F.COST_CLAIMS_YEAR), 0) AS TOTAL_CLAIMS_COST,
    NVL(AVG(F.PREMIUM), 0) AS AVERAGE_PREMIUM,
    NVL(SUM(F.EXPOSURE_TIME), 0) AS TOTAL_EXPOSURE
FROM DWH_GOLD.FACT_POLICY F
INNER JOIN DWH_GOLD.DIM_TIME T
    ON F.TIME_KEY = T.TIME_KEY
GROUP BY T.PERIOD
ORDER BY T.PERIOD
"""


@router.get("/yearly")
def get_dashboard_yearly():
    """
    Return yearly insurance portfolio KPIs from Gold FACT_POLICY.
    """

    connection = None

    try:
        connection = get_api_connection()

        with connection.cursor() as cursor:
            cursor.execute(YEARLY_SQL)
            rows = cursor.fetchall()

        years = [
            {
                "period": int(row[0]),
                "total_observations": int(row[1]),
                "total_policies": int(row[2]),
                "total_premium": float(row[3]),
                "total_claims_cost": float(row[4]),
                "average_premium": float(row[5]),
                "total_exposure": float(row[6]),
            }
            for row in rows
        ]

        return {"years": years}

    except Exception as exc:
        logger.exception("Dashboard yearly query failed.")

        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve yearly dashboard metrics.",
        ) from exc

    finally:
        if connection is not None:
            connection.close()
