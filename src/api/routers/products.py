"""
===============================================================================
Project : Insurance Risk Intelligence Platform
Module  : Dashboard Product Routes
Purpose : Expose product-level portfolio breakdowns.
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
    module_name="dashboard product routes",
)


PRODUCT_SQL = """
SELECT
    P.TYPE_PRODUCT,
    P.REIMBURSEMENT,
    COUNT(*) AS TOTAL_OBSERVATIONS,
    COUNT(DISTINCT F.ID_POLICY) AS TOTAL_POLICIES,
    NVL(SUM(F.PREMIUM), 0) AS TOTAL_PREMIUM,
    NVL(SUM(F.COST_CLAIMS_YEAR), 0) AS TOTAL_CLAIMS_COST,
    NVL(AVG(F.PREMIUM), 0) AS AVERAGE_PREMIUM,
    NVL(SUM(F.EXPOSURE_TIME), 0) AS TOTAL_EXPOSURE
FROM DWH_GOLD.FACT_POLICY F
INNER JOIN DWH_GOLD.DIM_PRODUCT P
    ON F.PRODUCT_KEY = P.PRODUCT_KEY
GROUP BY
    P.TYPE_PRODUCT,
    P.REIMBURSEMENT
ORDER BY
    P.TYPE_PRODUCT,
    P.REIMBURSEMENT
"""


@router.get("/products")
def get_dashboard_products():
    """
    Return portfolio KPIs grouped by product type and reimbursement.
    """

    connection = None

    try:
        connection = get_api_connection()

        with connection.cursor() as cursor:
            cursor.execute(PRODUCT_SQL)
            rows = cursor.fetchall()

        products = [
            {
                "type_product": row[0],
                "reimbursement": row[1],
                "total_observations": int(row[2]),
                "total_policies": int(row[3]),
                "total_premium": float(row[4]),
                "total_claims_cost": float(row[5]),
                "average_premium": float(row[6]),
                "total_exposure": float(row[7]),
            }
            for row in rows
        ]

        return {"products": products}

    except Exception as exc:
        logger.exception("Dashboard product breakdown query failed.")

        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve product dashboard metrics.",
        ) from exc

    finally:
        if connection is not None:
            connection.close()
