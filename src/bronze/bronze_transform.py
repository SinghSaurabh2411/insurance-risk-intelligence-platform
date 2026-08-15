"""
==========================================================
Project : Insurance Risk Intelligence Platform
Module  : Bronze Transformation
Author  : Saurabh Singh

Description
-----------
Transforms validated raw source data into the structure
required by the Bronze layer.

Responsibilities
----------------
1. Validate source DATE values.
2. Convert source DATE fields using the frozen source
   format: DD-MM-YYYY.
3. Convert NUMBER fields to appropriate Spark numeric
   types.
4. Preserve VARCHAR2 fields as strings.
5. Add ETL audit columns.
6. Generate RECORD_HASH.
7. Return the transformed Bronze DataFrame.

Frozen Grain
------------
ID_policy
ID_insured
period

Frozen Source Date Format
-------------------------
DD-MM-YYYY

Frozen Audit Columns
--------------------
LOAD_ID
LOAD_TIMESTAMP
SOURCE_FILE
RECORD_HASH
ETL_CREATED_BY

No Oracle write logic.
No MERGE logic.

==========================================================
"""

from typing import List

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import (
    IntegerType,
    DoubleType
)

from bronze.bronze_validator import (
    EXPECTED_SCHEMA,
    DATE_COLUMNS
)

from src.utils.hash_generator import (
    add_record_hash
)

from utils.logger import get_logger


# ==========================================================
# Logger
# ==========================================================

logger = get_logger(
    layer="bronze",
    module_name="bronze_transform"
)


# ==========================================================
# Frozen Source Date Format
# ==========================================================

SOURCE_DATE_FORMAT = "dd-MM-yyyy"


# ==========================================================
# Frozen Audit Columns
# ==========================================================

AUDIT_COLUMNS = [
    "LOAD_ID",
    "LOAD_TIMESTAMP",
    "SOURCE_FILE",
    "RECORD_HASH",
    "ETL_CREATED_BY"
]


# ==========================================================
# VARCHAR2 Columns
# ==========================================================

STRING_COLUMNS: List[str] = [
    column
    for column, data_type in EXPECTED_SCHEMA.items()
    if data_type == "VARCHAR2"
]


# ==========================================================
# Number Columns
# ==========================================================

NUMBER_COLUMNS: List[str] = [
    column
    for column, data_type in EXPECTED_SCHEMA.items()
    if data_type == "NUMBER"
]


# ==========================================================
# Validate and Transform Date Columns
# ==========================================================

def transform_date_columns(
    dataframe: DataFrame
) -> DataFrame:
    """
    Validates and converts source date columns.

    Frozen source format:

        DD-MM-YYYY

    Rules
    -----
    1. Blank values are treated as NULL.
    2. Valid DD-MM-YYYY values are converted to DateType.
    3. Non-blank invalid values cause the ETL to fail.

    Parameters
    ----------
    dataframe : DataFrame
        Raw validated DataFrame.

    Returns
    -------
    DataFrame
        DataFrame with converted date columns.

    Raises
    ------
    ValueError
        If a non-blank invalid date is detected.
    """

    logger.info(
        "Starting date validation and transformation "
        "using format: %s",
        SOURCE_DATE_FORMAT
    )

    transformed_df = dataframe

    for column in DATE_COLUMNS:

        # --------------------------------------------------
        # Preserve original source value
        # --------------------------------------------------

        raw_value = F.trim(
            F.col(column).cast("string")
        )

        # --------------------------------------------------
        # Parse the source date
        #
        # Empty string -> NULL
        # Valid date   -> DateType
        # Invalid date -> NULL
        # --------------------------------------------------

        parsed_date = F.to_date(
            F.when(
                raw_value == "",
                None
            ).otherwise(
                raw_value
            ),
            SOURCE_DATE_FORMAT
        )

        # --------------------------------------------------
        # Detect invalid non-blank values BEFORE replacing
        # the source column.
        # --------------------------------------------------

        invalid_count = (
            dataframe
            .filter(
                raw_value != ""
            )
            .filter(
                parsed_date.isNull()
            )
            .limit(1)
            .count()
        )

        if invalid_count > 0:

            logger.error(
                "Invalid date value detected in column: %s. "
                "Expected format: %s",
                column,
                SOURCE_DATE_FORMAT
            )

            raise ValueError(
                f"Invalid date value detected in column "
                f"'{column}'. Expected format: "
                f"{SOURCE_DATE_FORMAT}"
            )

        # --------------------------------------------------
        # Replace raw string with Spark DateType
        # --------------------------------------------------

        transformed_df = transformed_df.withColumn(
            column,
            parsed_date
        )

        logger.info(
            "Successfully transformed date column: %s",
            column
        )

    logger.info(
        "Date validation and transformation completed."
    )

    return transformed_df


# ==========================================================
# Transform Number Columns
# ==========================================================

def transform_number_columns(
    dataframe: DataFrame
) -> DataFrame:
    """
    Converts source numeric values into Spark numeric types.

    Parameters
    ----------
    dataframe : DataFrame
        Input DataFrame.

    Returns
    -------
    DataFrame
        DataFrame with numeric columns converted.
    """

    logger.info(
        "Starting numeric column transformation."
    )

    transformed_df = dataframe

    # ------------------------------------------------------
    # Integer-like columns
    # ------------------------------------------------------

    integer_columns = [
        "period",
        "year_effect_insured",
        "year_lapse_insured",
        "year_effect_policy",
        "year_lapse_policy",
        "lapse",
        "seniority_insured",
        "seniority_policy",
        "new_business",
        "age",
        "n_medical_services",
        "n_insured_pc",
        "n_insured_mun",
        "n_insured_prov",
        "IICIMUN",
        "C_GI",
        "C_II",
        "C_IE_P",
        "C_IE_S",
        "C_IE_T",
        "C_GE_P",
        "C_GE_S",
        "C_GE_T"
    ]

    # ------------------------------------------------------
    # Integer conversion
    # ------------------------------------------------------

    for column in integer_columns:

        if column in transformed_df.columns:

            transformed_df = transformed_df.withColumn(
                column,
                F.col(column).cast(IntegerType())
            )

    # ------------------------------------------------------
    # Decimal / floating-point columns
    # ------------------------------------------------------

    decimal_columns = [
        "exposure_time",
        "premium",
        "cost_claims_year"
    ]

    for column in decimal_columns:

        if column in transformed_df.columns:

            transformed_df = transformed_df.withColumn(
                column,
                F.col(column).cast(DoubleType())
            )

    logger.info(
        "Numeric column transformation completed."
    )

    return transformed_df


# ==========================================================
# Add Audit Columns
# ==========================================================

def add_audit_columns(
    dataframe: DataFrame,
    load_id: int,
    source_file: str,
    etl_created_by: str
) -> DataFrame:
    """
    Adds the frozen ETL audit columns.

    Parameters
    ----------
    dataframe : DataFrame
        Transformed DataFrame.

    load_id : int
        Unique ETL load identifier.

    source_file : str
        Source file name.

    etl_created_by : str
        ETL process responsible for the load.

    Returns
    -------
    DataFrame
        DataFrame containing audit columns.
    """

    logger.info(
        "Adding Bronze audit columns."
    )

    transformed_df = (
        dataframe
        .withColumn(
            "LOAD_ID",
            F.lit(load_id).cast(IntegerType())
        )
        .withColumn(
            "LOAD_TIMESTAMP",
            F.current_timestamp()
        )
        .withColumn(
            "SOURCE_FILE",
            F.lit(source_file)
        )
        .withColumn(
            "ETL_CREATED_BY",
            F.lit(etl_created_by)
        )
    )

    return transformed_df


# ==========================================================
# Generate Record Hash
# ==========================================================

def generate_record_hash(
    dataframe: DataFrame
) -> DataFrame:
    """
    Generates RECORD_HASH using all source business/data
    columns.

    Audit columns are deliberately excluded.

    Parameters
    ----------
    dataframe : DataFrame
        Transformed DataFrame.

    Returns
    -------
    DataFrame
        DataFrame containing RECORD_HASH.
    """

    hash_columns = [
        column
        for column in EXPECTED_SCHEMA.keys()
        if column in dataframe.columns
    ]

    logger.info(
        "Generating RECORD_HASH using %d source columns.",
        len(hash_columns)
    )

    return add_record_hash(
        dataframe=dataframe,
        columns=hash_columns,
        hash_column="RECORD_HASH"
    )


# ==========================================================
# Complete Bronze Transformation
# ==========================================================

def transform_to_bronze(
    dataframe: DataFrame,
    load_id: int,
    source_file: str,
    etl_created_by: str
) -> DataFrame:
    """
    Executes the complete Bronze transformation.

    Processing order
    ----------------
    1. Validate and convert DATE columns
    2. Convert NUMBER columns
    3. Generate RECORD_HASH
    4. Add audit columns

    Parameters
    ----------
    dataframe : DataFrame
        Validated raw source DataFrame.

    load_id : int
        ETL load identifier.

    source_file : str
        Source file name.

    etl_created_by : str
        ETL process identifier.

    Returns
    -------
    DataFrame
        Bronze-ready DataFrame.
    """

    logger.info(
        "Starting Bronze transformation for file: %s",
        source_file
    )

    # ------------------------------------------------------
    # 1. Date Validation + Transformation
    # ------------------------------------------------------

    transformed_df = transform_date_columns(
        dataframe
    )

    # ------------------------------------------------------
    # 2. Numeric Transformation
    # ------------------------------------------------------

    transformed_df = transform_number_columns(
        transformed_df
    )

    # ------------------------------------------------------
    # 3. Generate RECORD_HASH
    # ------------------------------------------------------

    transformed_df = generate_record_hash(
        transformed_df
    )

    # ------------------------------------------------------
    # 4. Add Audit Columns
    # ------------------------------------------------------

    transformed_df = add_audit_columns(
        transformed_df,
        load_id=load_id,
        source_file=source_file,
        etl_created_by=etl_created_by
    )

    logger.info(
        "Bronze transformation completed for file: %s",
        source_file
    )

    return transformed_df