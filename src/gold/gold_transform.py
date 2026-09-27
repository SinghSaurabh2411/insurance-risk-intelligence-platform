from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window

def _single_row_per_key(df: DataFrame, keys: list[str]) -> DataFrame:
    window = Window.partitionBy(*keys).orderBy(F.col("PERIOD").desc())
    return (
        df.withColumn("_rn", F.row_number().over(window))
          .filter(F.col("_rn") == 1)
          .drop("_rn")
    )

def build_dimensions(
    customer: DataFrame,
    policy: DataFrame,
    product: DataFrame,
    channel: DataFrame,
    time: DataFrame,
):
    customer_dim = (
        _single_row_per_key(customer, ["ID_POLICY", "ID_INSURED"])
        .select(
            "ID_POLICY", "ID_INSURED",
            "DATE_EFFECT_INSURED", "DATE_LAPSE_INSURED",
            "YEAR_EFFECT_INSURED", "YEAR_LAPSE_INSURED", "GENDER"
        )
    )

    policy_dim = (
        _single_row_per_key(policy, ["ID_POLICY"])
        .select(
            "ID_POLICY", "TYPE_POLICY", "TYPE_POLICY_DG",
            "DATE_EFFECT_POLICY", "DATE_LAPSE_POLICY",
            "YEAR_EFFECT_POLICY", "YEAR_LAPSE_POLICY"
        )
    )

    product_dim = (
        product.select("TYPE_PRODUCT", "REIMBURSEMENT")
               .distinct()
    )

    channel_dim = (
        channel.select("DISTRIBUTION_CHANNEL")
               .distinct()
    )

    time_dim = time.select("PERIOD").distinct()

    return customer_dim, policy_dim, product_dim, channel_dim, time_dim

def build_fact(
    policy: DataFrame,
    customer: DataFrame,
    product: DataFrame,
    channel: DataFrame,
    coverage: DataFrame,
    financial: DataFrame,
    record: DataFrame,
    dim_customer: DataFrame,
    dim_policy: DataFrame,
    dim_product: DataFrame,
    dim_channel: DataFrame,
    dim_time: DataFrame,
) -> DataFrame:
    fact = (
        record.select(
            "ID_POLICY", "ID_INSURED", "PERIOD",
            "LOAD_ID", "LOAD_TIMESTAMP", "SOURCE_FILE",
            "RECORD_HASH", "ETL_CREATED_BY"
        )
        .join(customer.select(
            "ID_POLICY", "ID_INSURED", "PERIOD",
            "AGE", "SENIORITY_INSURED"
        ), ["ID_POLICY", "ID_INSURED", "PERIOD"], "inner")
        .join(policy.select(
            "ID_POLICY", "ID_INSURED", "PERIOD",
            "SENIORITY_POLICY", "NEW_BUSINESS", "LAPSE"
        ), ["ID_POLICY", "ID_INSURED", "PERIOD"], "inner")
        .join(product.select(
            "ID_POLICY", "ID_INSURED", "PERIOD",
            "TYPE_PRODUCT", "REIMBURSEMENT"
        ), ["ID_POLICY", "ID_INSURED", "PERIOD"], "inner")
        .join(channel.select(
            "ID_POLICY", "ID_INSURED", "PERIOD",
            "DISTRIBUTION_CHANNEL"
        ), ["ID_POLICY", "ID_INSURED", "PERIOD"], "inner")
        .join(coverage.select(
            "ID_POLICY", "ID_INSURED", "PERIOD",
            "EXPOSURE_TIME", "N_MEDICAL_SERVICES"
        ), ["ID_POLICY", "ID_INSURED", "PERIOD"], "inner")
        .join(financial.select(
            "ID_POLICY", "ID_INSURED", "PERIOD",
            "PREMIUM", "COST_CLAIMS_YEAR"
        ), ["ID_POLICY", "ID_INSURED", "PERIOD"], "inner")
        .join(dim_customer.select("CUSTOMER_KEY", "ID_POLICY", "ID_INSURED"),
              ["ID_POLICY", "ID_INSURED"], "inner")
        .join(dim_policy.select("POLICY_KEY", "ID_POLICY"),
              ["ID_POLICY"], "inner")
        .join(dim_product.select("PRODUCT_KEY", "TYPE_PRODUCT", "REIMBURSEMENT"),
              ["TYPE_PRODUCT", "REIMBURSEMENT"], "inner")
        .join(dim_channel.select("CHANNEL_KEY", "DISTRIBUTION_CHANNEL"),
              ["DISTRIBUTION_CHANNEL"], "inner")
        .join(dim_time.select("TIME_KEY", "PERIOD"),
              ["PERIOD"], "inner")
        .select(
            "POLICY_KEY", "CUSTOMER_KEY", "PRODUCT_KEY", "CHANNEL_KEY", "TIME_KEY",
            "ID_POLICY", "ID_INSURED", "PERIOD",
            "PREMIUM", "COST_CLAIMS_YEAR", "EXPOSURE_TIME",
            "N_MEDICAL_SERVICES", "AGE", "SENIORITY_POLICY",
            "SENIORITY_INSURED", "NEW_BUSINESS", "LAPSE",
            "LOAD_ID", "LOAD_TIMESTAMP", "SOURCE_FILE",
            "RECORD_HASH", "ETL_CREATED_BY"
        )
    )
    return fact
