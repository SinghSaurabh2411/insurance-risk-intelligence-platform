from typing import Dict
from pyspark.sql import DataFrame
from config.config import AUDIT_COLUMNS, SILVER_MERGE_KEY
from bronze.bronze_validator import EXPECTED_SCHEMA
from utils.logger import get_logger

logger = get_logger(layer="silver", module_name="silver_transform")

SILVER_PROJECTIONS: Dict[str, list] = {
    "SILVER_RECORD": ["ID","ID_policy","ID_insured","period","RECORD_HASH","LOAD_ID","LOAD_TIMESTAMP","SOURCE_FILE","ETL_CREATED_BY"],
    "SILVER_TIME": ["period","year_effect_insured","year_lapse_insured","year_effect_policy","year_lapse_policy"],
    "SILVER_POLICY": ["ID_policy","ID_insured","period","date_effect_policy","date_lapse_policy","seniority_policy","type_policy","type_policy_dg","new_business","lapse"],
    "SILVER_CUSTOMER": ["ID_insured","ID_policy","period","date_effect_insured","date_lapse_insured","seniority_insured","gender","age"],
    "SILVER_PRODUCT": ["ID_policy","ID_insured","period","type_product","reimbursement"],
    "SILVER_CHANNEL": ["ID_policy","ID_insured","period","distribution_channel"],
    "SILVER_COVERAGE": ["ID_policy","ID_insured","period","exposure_time","n_medical_services"],
    "SILVER_FINANCIAL": ["ID_policy","ID_insured","period","premium","cost_claims_year"],
}

def validate_projection_definitions() -> None:
    source_columns = set(EXPECTED_SCHEMA) | set(AUDIT_COLUMNS)
    for table_name, columns in SILVER_PROJECTIONS.items():
        missing = [c for c in columns if c not in source_columns]
        if missing:
            raise ValueError(f"{table_name} contains unavailable columns: {missing}")
        if table_name != "SILVER_TIME" and not set(SILVER_MERGE_KEY).issubset(columns):
            raise ValueError(f"{table_name} must contain {SILVER_MERGE_KEY}")

def project_silver_tables(bronze_dataframe: DataFrame) -> Dict[str, DataFrame]:
    validate_projection_definitions()
    projections = {}
    for table_name, columns in SILVER_PROJECTIONS.items():
        missing = [c for c in columns if c not in bronze_dataframe.columns]
        if missing:
            raise ValueError(f"Bronze DataFrame missing {table_name} columns: {missing}")
        projections[table_name] = bronze_dataframe.select(*columns)
    logger.info("Created %d approved Silver projections.", len(projections))
    return projections
