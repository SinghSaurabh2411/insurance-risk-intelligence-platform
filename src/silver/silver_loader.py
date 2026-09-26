from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from config.config import BRONZE_POLICY_TABLE_FQN
from config.oracle_config import BRONZE_JDBC_PROPERTIES, SILVER_JDBC_PROPERTIES, JDBC_URL
from utils.oracle_helper import read_table, execute_sql
from utils.logger import get_logger
from silver.silver_transform import project_silver_tables, SILVER_PROJECTIONS
from silver.silver_validator import validate_all_projections
from silver.silver_merge import merge_all_silver_tables

logger = get_logger(layer="silver", module_name="silver_loader")
STAGE = "DWH_SILVER.SILVER_STAGE"

STAGE_COLUMNS = [
    "ID","ID_policy","ID_insured","period",
    "date_effect_insured","date_lapse_insured","date_effect_policy","date_lapse_policy",
    "year_effect_insured","year_lapse_insured","year_effect_policy","year_lapse_policy",
    "exposure_time","lapse","seniority_insured","seniority_policy",
    "type_policy","type_policy_dg","type_product","reimbursement","new_business",
    "distribution_channel","gender","age","premium","cost_claims_year","n_medical_services",
    "RECORD_HASH","LOAD_ID","LOAD_TIMESTAMP","SOURCE_FILE","ETL_CREATED_BY",
]

def _clear_stage():
    execute_sql(f"TRUNCATE TABLE {STAGE}", SILVER_JDBC_PROPERTIES)

def _write_stage(df: DataFrame):
    (df.write.format("jdbc").option("url",JDBC_URL).option("dbtable",STAGE)
       .option("user",SILVER_JDBC_PROPERTIES["user"])
       .option("password",SILVER_JDBC_PROPERTIES["password"])
       .option("driver",SILVER_JDBC_PROPERTIES["driver"]).mode("append").save())

def run_silver_pipeline(spark: SparkSession) -> None:
    logger.info("Starting Silver ETL pipeline.")
    bronze = read_table(spark, BRONZE_POLICY_TABLE_FQN, BRONZE_JDBC_PROPERTIES)
    logger.info("Bronze rows read for Silver: %d", bronze.count())
    projections = project_silver_tables(bronze)
    validate_all_projections(projections)
    _clear_stage()
    _write_stage(bronze.select(*STAGE_COLUMNS))
    merge_all_silver_tables(SILVER_PROJECTIONS)
    logger.info("Silver ETL pipeline completed successfully.")
