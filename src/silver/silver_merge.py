from typing import Dict
from config.config import (
    SILVER_RECORD_TABLE_FQN,SILVER_TIME_TABLE_FQN,SILVER_POLICY_TABLE_FQN,
    SILVER_CUSTOMER_TABLE_FQN,SILVER_PRODUCT_TABLE_FQN,SILVER_CHANNEL_TABLE_FQN,
    SILVER_COVERAGE_TABLE_FQN,SILVER_FINANCIAL_TABLE_FQN,
)
from config.oracle_config import SILVER_JDBC_PROPERTIES
from utils.oracle_helper import execute_sql
from utils.logger import get_logger

logger = get_logger(layer="silver", module_name="silver_merge")
STAGE = "DWH_SILVER.SILVER_STAGE"
TARGETS = {
    "SILVER_RECORD": SILVER_RECORD_TABLE_FQN,
    "SILVER_TIME": SILVER_TIME_TABLE_FQN,
    "SILVER_POLICY": SILVER_POLICY_TABLE_FQN,
    "SILVER_CUSTOMER": SILVER_CUSTOMER_TABLE_FQN,
    "SILVER_PRODUCT": SILVER_PRODUCT_TABLE_FQN,
    "SILVER_CHANNEL": SILVER_CHANNEL_TABLE_FQN,
    "SILVER_COVERAGE": SILVER_COVERAGE_TABLE_FQN,
    "SILVER_FINANCIAL": SILVER_FINANCIAL_TABLE_FQN,
}

def _sql(target: str, columns: list, keys: list) -> str:
    non_keys = [c for c in columns if c not in keys]
    on = " AND ".join(f"t.{c.upper()} = s.{c.upper()}" for c in keys)
    updates = ", ".join(f"t.{c.upper()} = s.{c.upper()}" for c in non_keys)
    ins_cols = ", ".join(c.upper() for c in columns)
    ins_vals = ", ".join(f"s.{c.upper()}" for c in columns)
    using_source = STAGE
    if target.endswith("SILVER_TIME"):
        using_source = f"(SELECT DISTINCT {\", \".join(c.upper() for c in columns)} FROM {STAGE})"
    return f"""MERGE INTO {target} t
USING {using_source} s
ON ({on})
WHEN MATCHED THEN UPDATE SET {updates}
WHEN NOT MATCHED THEN INSERT ({ins_cols}) VALUES ({ins_vals})"""

def merge_all_silver_tables(projection_columns: Dict[str, list]) -> None:
    order = ["SILVER_RECORD","SILVER_TIME","SILVER_POLICY","SILVER_CUSTOMER","SILVER_PRODUCT","SILVER_CHANNEL","SILVER_COVERAGE","SILVER_FINANCIAL"]
    for name in order:
        keys = ["period"] if name == "SILVER_TIME" else ["ID_policy","ID_insured","period"]
        logger.info("Executing Oracle MERGE | target=%s", name)
        execute_sql(_sql(TARGETS[name], projection_columns[name], keys), SILVER_JDBC_PROPERTIES)
