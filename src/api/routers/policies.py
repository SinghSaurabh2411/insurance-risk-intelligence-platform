"""
===============================================================================
Project : Insurance Risk Intelligence Platform
Module  : Dashboard Policy Routes
Purpose : Expose policy-type portfolio breakdowns.
===============================================================================
"""

from fastapi import APIRouter, Depends, HTTPException

from api.security import require_api_key
from api.models import PoliciesResponse

from api.database import get_api_connection
from utils.logger import get_logger


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(require_api_key)],
)

logger = get_logger(
    layer="api",
    module_name="dashboard policy routes",
)


POLICY_SQL = """
SELECT
    P.TYPE_POLICY,
    P.TYPE_POLICY_DG,
    COUNT(*) AS TOTAL_OBSERVATIONS,
    COUNT(DISTINCT F.ID_POLICY) AS TOTAL_POLICIES,
    NVL(SUM(F.PREMIUM), 0) AS TOTAL_PREMIUM,
    NVL(SUM(F.COST_CLAIMS_YEAR), 0) AS TOTAL_CLAIMS_COST,
    NVL(AVG(F.PREMIUM), 0) AS AVERAGE_PREMIUM,
    NVL(SUM(F.EXPOSURE_TIME), 0) AS TOTAL_EXPOSURE
FROM DWH_GOLD.FACT_POLICY F
INNER JOIN DWH_GOLD.DIM_POLICY P
    ON F.POLICY_KEY = P.POLICY_KEY
GROUP BY
    P.TYPE_POLICY,
    P.TYPE_POLICY_DG
ORDER BY
    P.TYPE_POLICY,
    P.TYPE_POLICY_DG
"""


@router.get("/policies", response_model=PoliciesResponse)
def get_dashboard_policies():
    """
    Return portfolio KPIs grouped by policy type and policy DG type.
    """

    connection = None

    try:
        connection = get_api_connection()

        with connection.cursor() as cursor:
            cursor.execute(POLICY_SQL)
            rows = cursor.fetchall()

        policies = [
            {
                "type_policy": row[0],
                "type_policy_dg": row[1],
                "total_observations": int(row[2]),
                "total_policies": int(row[3]),
                "total_premium": float(row[4]),
                "total_claims_cost": float(row[5]),
                "average_premium": float(row[6]),
                "total_exposure": float(row[7]),
            }
            for row in rows
        ]

        return {"policies": policies}

    except Exception as exc:
        logger.exception("Dashboard policy breakdown query failed.")

        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve policy dashboard metrics.",
        ) from exc

    finally:
        if connection is not None:
            connection.close()
