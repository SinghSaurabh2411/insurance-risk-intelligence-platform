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
SELECT
    COUNT(DISTINCT F.ID_POLICY) AS TOTAL_POLICIES,
    COUNT(*) AS TOTAL_OBSERVATIONS,
    NVL(SUM(F.PREMIUM), 0) AS TOTAL_PREMIUM,
    NVL(SUM(F.COST_CLAIMS_YEAR), 0) AS TOTAL_CLAIMS_COST,
    NVL(AVG(F.PREMIUM), 0) AS AVERAGE_PREMIUM,
    NVL(SUM(F.EXPOSURE_TIME), 0) AS TOTAL_EXPOSURE
FROM DWH_GOLD.FACT_POLICY F
"""


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


@router.get("/channels")
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
