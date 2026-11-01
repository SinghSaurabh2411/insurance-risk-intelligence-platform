"""
===============================================================================
Project : Insurance Risk Intelligence Platform
Module  : Dashboard Channel Routes
Purpose : Expose distribution-channel portfolio breakdowns.
===============================================================================
"""

from fastapi import APIRouter, Depends, HTTPException

from api.security import require_api_key
from api.models import ChannelsResponse

from api.database import get_api_connection
from utils.logger import get_logger


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(require_api_key)],
)

logger = get_logger(
    layer="api",
    module_name="dashboard channel routes",
)


CHANNEL_SQL = """
SELECT
    C.DISTRIBUTION_CHANNEL,
    COUNT(*) AS TOTAL_OBSERVATIONS,
    COUNT(DISTINCT F.ID_POLICY) AS TOTAL_POLICIES,
    NVL(SUM(F.PREMIUM), 0) AS TOTAL_PREMIUM,
    NVL(SUM(F.COST_CLAIMS_YEAR), 0) AS TOTAL_CLAIMS_COST,
    NVL(AVG(F.PREMIUM), 0) AS AVERAGE_PREMIUM,
    NVL(SUM(F.EXPOSURE_TIME), 0) AS TOTAL_EXPOSURE
FROM DWH_GOLD.FACT_POLICY F
INNER JOIN DWH_GOLD.DIM_CHANNEL C
    ON F.CHANNEL_KEY = C.CHANNEL_KEY
GROUP BY C.DISTRIBUTION_CHANNEL
ORDER BY C.DISTRIBUTION_CHANNEL
"""


@router.get("/channels", response_model=ChannelsResponse)
def get_dashboard_channels():
    """
    Return portfolio KPIs grouped by distribution channel.
    """

    connection = None

    try:
        connection = get_api_connection()

        with connection.cursor() as cursor:
            cursor.execute(CHANNEL_SQL)
            rows = cursor.fetchall()

        channels = [
            {
                "distribution_channel": row[0],
                "total_observations": int(row[1]),
                "total_policies": int(row[2]),
                "total_premium": float(row[3]),
                "total_claims_cost": float(row[4]),
                "average_premium": float(row[5]),
                "total_exposure": float(row[6]),
            }
            for row in rows
        ]

        return {"channels": channels}

    except Exception as exc:
        logger.exception("Dashboard channel breakdown query failed.")

        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve channel dashboard metrics.",
        ) from exc

    finally:
        if connection is not None:
            connection.close()
