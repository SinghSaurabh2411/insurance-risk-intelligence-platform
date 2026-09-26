from typing import Dict
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from config.config import SILVER_MERGE_KEY
from utils.logger import get_logger

logger = get_logger(layer="silver", module_name="silver_validator")

def _not_null(df: DataFrame, columns: list) -> None:
    condition = None
    for column in columns:
        current = F.col(column).isNull()
        condition = current if condition is None else condition | current
    if df.filter(condition).limit(1).count() > 0:
        raise ValueError(f"NULL business-key value detected: {columns}")

def _unique(df: DataFrame, columns: list) -> None:
    if df.groupBy(*columns).count().filter(F.col("count") > 1).limit(1).count() > 0:
        raise ValueError(f"Duplicate Silver keys detected: {columns}")

def validate_projection(table_name: str, dataframe: DataFrame) -> None:
    if dataframe.limit(1).count() == 0:
        raise ValueError(f"{table_name} contains no records.")
    key = ["period"] if table_name == "SILVER_TIME" else SILVER_MERGE_KEY
    _not_null(dataframe, key)
    _unique(dataframe, key)
    logger.info("Silver DQ passed | table=%s", table_name)

def validate_all_projections(projections: Dict[str, DataFrame]) -> None:
    for name, df in projections.items():
        validate_projection(name, df)
