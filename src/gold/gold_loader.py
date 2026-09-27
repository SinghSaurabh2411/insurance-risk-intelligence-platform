from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window

from config.config import (
    GOLD_SCHEMA,
    DIM_CUSTOMER_FQN, DIM_POLICY_FQN, DIM_PRODUCT_FQN,
    DIM_CHANNEL_FQN, DIM_TIME_FQN, FACT_POLICY_FQN
)
from config.oracle_config import SILVER_JDBC_PROPERTIES, GOLD_JDBC_PROPERTIES, JDBC_URL
from utils.oracle_helper import read_table, execute_sql
from utils.logger import get_logger
from gold.gold_transform import build_dimensions, build_fact

logger = get_logger(layer="gold", module_name="gold_loader")
STAGE = f"{GOLD_SCHEMA}.GOLD_STAGE"

SILVER_TABLES = {
    "record": "DWH_SILVER.SILVER_RECORD",
    "time": "DWH_SILVER.SILVER_TIME",
    "policy": "DWH_SILVER.SILVER_POLICY",
    "customer": "DWH_SILVER.SILVER_CUSTOMER",
    "product": "DWH_SILVER.SILVER_PRODUCT",
    "channel": "DWH_SILVER.SILVER_CHANNEL",
    "coverage": "DWH_SILVER.SILVER_COVERAGE",
    "financial": "DWH_SILVER.SILVER_FINANCIAL",
}

def _write_jdbc(df: DataFrame, table: str) -> None:
    (
        df.write.format("jdbc")
          .option("url", JDBC_URL)
          .option("dbtable", table)
          .option("user", GOLD_JDBC_PROPERTIES["user"])
          .option("password", GOLD_JDBC_PROPERTIES["password"])
          .option("driver", GOLD_JDBC_PROPERTIES["driver"])
          .mode("append")
          .save()
    )

def _clear_gold() -> None:
    # Gold is currently a full-refresh analytical layer. The fact is cleared
    # first so dimension foreign keys can be safely rebuilt.
    for table in (
        FACT_POLICY_FQN,
        DIM_CUSTOMER_FQN,
        DIM_POLICY_FQN,
        DIM_PRODUCT_FQN,
        DIM_CHANNEL_FQN,
        DIM_TIME_FQN,
        STAGE,
    ):
        execute_sql(f"TRUNCATE TABLE {table}", GOLD_JDBC_PROPERTIES)

def _load_dimensions(dims):
    customer, policy, product, channel, time = dims

    customer_stage = customer.withColumn(
        "CUSTOMER_KEY", F.row_number().over(Window.orderBy("ID_POLICY", "ID_INSURED"))
    )
    policy_stage = policy.withColumn(
        "POLICY_KEY", F.row_number().over(Window.orderBy("ID_POLICY"))
    )
    product_stage = product.withColumn(
        "PRODUCT_KEY", F.row_number().over(Window.orderBy("TYPE_PRODUCT", "REIMBURSEMENT"))
    )
    channel_stage = channel.withColumn(
        "CHANNEL_KEY", F.row_number().over(Window.orderBy("DISTRIBUTION_CHANNEL"))
    )
    time_stage = time.withColumn(
        "TIME_KEY", F.row_number().over(Window.orderBy("PERIOD"))
    )

    audit = [
        F.current_timestamp().alias("CREATED_TIMESTAMP"),
        F.current_timestamp().alias("UPDATED_TIMESTAMP"),
        F.lit("PYSPARK_ETL").alias("ETL_CREATED_BY"),
    ]

    customer_stage = customer_stage.select("*", *audit)
    policy_stage = policy_stage.select("*", *audit)
    product_stage = product_stage.select("*", *audit)
    channel_stage = channel_stage.select("*", *audit)
    time_stage = time_stage.select("*", *audit)

    _write_jdbc(
        customer_stage.select(
            "CUSTOMER_KEY", "ID_POLICY", "ID_INSURED",
            "DATE_EFFECT_INSURED", "DATE_LAPSE_INSURED",
            "YEAR_EFFECT_INSURED", "YEAR_LAPSE_INSURED", "GENDER",
            "CREATED_TIMESTAMP", "UPDATED_TIMESTAMP", "ETL_CREATED_BY"
        ), DIM_CUSTOMER_FQN
    )
    _write_jdbc(
        policy_stage.select(
            "POLICY_KEY", "ID_POLICY", "TYPE_POLICY", "TYPE_POLICY_DG",
            "DATE_EFFECT_POLICY", "DATE_LAPSE_POLICY",
            "YEAR_EFFECT_POLICY", "YEAR_LAPSE_POLICY",
            "CREATED_TIMESTAMP", "UPDATED_TIMESTAMP", "ETL_CREATED_BY"
        ), DIM_POLICY_FQN
    )
    _write_jdbc(
        product_stage.select(
            "PRODUCT_KEY", "TYPE_PRODUCT", "REIMBURSEMENT",
            "CREATED_TIMESTAMP", "UPDATED_TIMESTAMP", "ETL_CREATED_BY"
        ), DIM_PRODUCT_FQN
    )
    _write_jdbc(
        channel_stage.select(
            "CHANNEL_KEY", "DISTRIBUTION_CHANNEL",
            "CREATED_TIMESTAMP", "UPDATED_TIMESTAMP", "ETL_CREATED_BY"
        ), DIM_CHANNEL_FQN
    )
    _write_jdbc(
        time_stage.select(
            "TIME_KEY", "PERIOD",
            "CREATED_TIMESTAMP", "UPDATED_TIMESTAMP", "ETL_CREATED_BY"
        ), DIM_TIME_FQN
    )

    return customer_stage, policy_stage, product_stage, channel_stage, time_stage

def run_gold_pipeline(spark: SparkSession) -> None:
    logger.info("Starting Gold ETL pipeline.")

    record = read_table(spark, SILVER_TABLES["record"], SILVER_JDBC_PROPERTIES)
    time = read_table(spark, SILVER_TABLES["time"], SILVER_JDBC_PROPERTIES)
    policy = read_table(spark, SILVER_TABLES["policy"], SILVER_JDBC_PROPERTIES)
    customer = read_table(spark, SILVER_TABLES["customer"], SILVER_JDBC_PROPERTIES)
    product = read_table(spark, SILVER_TABLES["product"], SILVER_JDBC_PROPERTIES)
    channel = read_table(spark, SILVER_TABLES["channel"], SILVER_JDBC_PROPERTIES)
    coverage = read_table(spark, SILVER_TABLES["coverage"], SILVER_JDBC_PROPERTIES)
    financial = read_table(spark, SILVER_TABLES["financial"], SILVER_JDBC_PROPERTIES)

    _clear_gold()

    dims = build_dimensions(customer, policy, product, channel, time)
    dim_customer, dim_policy, dim_product, dim_channel, dim_time = _load_dimensions(dims)

    fact = build_fact(
        policy, customer, product, channel, coverage, financial, record,
        dim_customer, dim_policy, dim_product, dim_channel, dim_time
    )

    _write_jdbc(fact, FACT_POLICY_FQN)

    logger.info("Gold ETL pipeline completed successfully. Fact rows: %d", fact.count())
