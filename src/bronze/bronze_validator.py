"""
==========================================================
Project : Insurance Risk Intelligence Platform
Module  : Bronze Validator
Author  : Saurabh Singh

Description
-----------
Validates the incoming source data before it enters the
Bronze layer.

Validation covers:

1. Required columns
2. Unexpected columns
3. Expected source data types
4. Business-key NULL checks
5. Duplicate business keys
6. Basic structural validation

Frozen Grain
------------
ID_policy
ID_insured
period

Important
---------
The source file is expected to be read as raw data.

Therefore:

- DATE fields may arrive as STRING.
- NUMBER fields may arrive as STRING.
- Explicit type conversion is performed later by
  bronze_transform.py.

The validator does NOT assume or guess the source date
format.

No Oracle write logic.
No MERGE logic.
No transformation logic.

==========================================================
"""

from typing import Dict, List

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

from src.utils.logger import get_logger


# ==========================================================
# Logger
# ==========================================================

logger = get_logger(
    layer="bronze",
    module_name="bronze_validator"
)


# ==========================================================
# Frozen Business Grain
# ==========================================================

BUSINESS_KEY_COLUMNS = [
    "ID_policy",
    "ID_insured",
    "period"
]


# ==========================================================
# Frozen Data Dictionary
# ==========================================================

EXPECTED_SCHEMA: Dict[str, str] = {

    "ID": "VARCHAR2",
    "ID_policy": "VARCHAR2",
    "ID_insured": "VARCHAR2",

    "period": "NUMBER",

    "date_effect_insured": "DATE",
    "date_lapse_insured": "DATE",
    "date_effect_policy": "DATE",
    "date_lapse_policy": "DATE",

    "year_effect_insured": "NUMBER",
    "year_lapse_insured": "NUMBER",
    "year_effect_policy": "NUMBER",
    "year_lapse_policy": "NUMBER",

    "exposure_time": "NUMBER",
    "lapse": "NUMBER",

    "seniority_insured": "NUMBER",
    "seniority_policy": "NUMBER",

    "type_policy": "VARCHAR2",
    "type_policy_dg": "VARCHAR2",
    "type_product": "VARCHAR2",
    "reimbursement": "VARCHAR2",

    "new_business": "NUMBER",

    "distribution_channel": "VARCHAR2",
    "gender": "VARCHAR2",

    "age": "NUMBER",

    "premium": "NUMBER",
    "cost_claims_year": "NUMBER",
    "n_medical_services": "NUMBER",

    "n_insured_pc": "NUMBER",
    "n_insured_mun": "NUMBER",
    "n_insured_prov": "NUMBER",

    "IICIMUN": "NUMBER",
    "IICIPROV": "NUMBER",

    "C_H": "VARCHAR2",

    "C_GI": "NUMBER",
    "C_II": "NUMBER",

    "C_IE_P": "NUMBER",
    "C_IE_S": "NUMBER",
    "C_IE_T": "NUMBER",

    "C_GE_P": "NUMBER",
    "C_GE_S": "NUMBER",
    "C_GE_T": "NUMBER",

    "C_C": "VARCHAR2"
}


# ==========================================================
# Expected Column Order
# ==========================================================

EXPECTED_COLUMNS: List[str] = list(
    EXPECTED_SCHEMA.keys()
)


# ==========================================================
# Columns Requiring Explicit Conversion
# ==========================================================

DATE_COLUMNS = [
    "date_effect_insured",
    "date_lapse_insured",
    "date_effect_policy",
    "date_lapse_policy"
]


NUMBER_COLUMNS = [
    column
    for column, data_type in EXPECTED_SCHEMA.items()
    if data_type == "NUMBER"
]


# ==========================================================
# Schema / Column Validation
# ==========================================================

def validate_columns(
    dataframe: DataFrame
) -> None:
    """
    Validates the source DataFrame columns.

    Checks:
    - Missing columns
    - Unexpected columns
    - Column order

    Parameters
    ----------
    dataframe : DataFrame
        Input source DataFrame.

    Raises
    ------
    ValueError
        If column validation fails.
    """

    actual_columns = dataframe.columns

    # ------------------------------------------------------
    # Missing Columns
    # ------------------------------------------------------

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in actual_columns
    ]

    if missing_columns:

        logger.error(
            "Missing required columns: %s",
            missing_columns
        )

        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # ------------------------------------------------------
    # Unexpected Columns
    # ------------------------------------------------------

    unexpected_columns = [
        column
        for column in actual_columns
        if column not in EXPECTED_COLUMNS
    ]

    if unexpected_columns:

        logger.error(
            "Unexpected columns detected: %s",
            unexpected_columns
        )

        raise ValueError(
            f"Unexpected columns detected: "
            f"{unexpected_columns}"
        )

    # ------------------------------------------------------
    # Column Order
    # ------------------------------------------------------

    if actual_columns != EXPECTED_COLUMNS:

        logger.error(
            "Column order does not match the frozen "
            "Data Dictionary."
        )

        raise ValueError(
            "Column order does not match the frozen "
            "Data Dictionary."
        )

    logger.info(
        "Column validation successful."
    )


# ==========================================================
# Source Data Type Validation
# ==========================================================

def validate_source_data_types(
    dataframe: DataFrame
) -> None:
    """
    Validates the raw source DataFrame types.

    Since the source is a CSV file, values may initially
    arrive as strings.

    Therefore:

    - VARCHAR2 -> STRING expected
    - DATE     -> STRING expected
    - NUMBER   -> STRING expected

    Actual DATE and NUMBER conversion is deliberately
    handled later by bronze_transform.py.

    Parameters
    ----------
    dataframe : DataFrame
        Raw source DataFrame.

    Raises
    ------
    ValueError
        If an unexpected source type is detected.
    """

    actual_schema = {
        field.name: field.dataType
        for field in dataframe.schema.fields
    }

    type_errors = []

    for column, expected_type in EXPECTED_SCHEMA.items():

        actual_type = actual_schema[column]

        # --------------------------------------------------
        # CSV source representation
        # --------------------------------------------------

        if not isinstance(actual_type, StringType):

            type_errors.append(
                {
                    "column": column,
                    "logical_type": expected_type,
                    "actual_source_type": str(actual_type)
                }
            )

    if type_errors:

        logger.error(
            "Unexpected source data types detected: %s",
            type_errors
        )

        raise ValueError(
            "Source data type validation failed: "
            f"{type_errors}"
        )

    logger.info(
        "Source data type validation successful."
    )


# ==========================================================
# Business Key NULL Validation
# ==========================================================

def validate_business_key_nulls(
    dataframe: DataFrame
) -> None:
    """
    Validates that frozen business-key columns do not
    contain NULL or empty values.

    Frozen grain:

        ID_policy
        ID_insured
        period

    Parameters
    ----------
    dataframe : DataFrame
        Input source DataFrame.

    Raises
    ------
    ValueError
        If NULL or empty business-key values are detected.
    """

    null_condition = None

    for column in BUSINESS_KEY_COLUMNS:

        condition = (
            F.col(column).isNull()
            |
            (
                F.trim(
                    F.col(column).cast("string")
                ) == ""
            )
        )

        if null_condition is None:

            null_condition = condition

        else:

            null_condition = (
                null_condition | condition
            )

    invalid_count = (
        dataframe
        .filter(null_condition)
        .limit(1)
        .count()
    )

    if invalid_count > 0:

        logger.error(
            "NULL or empty values detected in "
            "business-key columns."
        )

        raise ValueError(
            "NULL or empty values detected in "
            f"business-key columns: "
            f"{BUSINESS_KEY_COLUMNS}"
        )

    logger.info(
        "Business-key NULL validation successful."
    )


# ==========================================================
# Duplicate Business Key Validation
# ==========================================================

def validate_business_key_duplicates(
    dataframe: DataFrame
) -> None:
    """
    Validates uniqueness of the frozen business grain.

    Grain:

        ID_policy
        ID_insured
        period

    Parameters
    ----------
    dataframe : DataFrame
        Input source DataFrame.

    Raises
    ------
    ValueError
        If duplicate business keys are detected.
    """

    duplicate_count = (
        dataframe
        .groupBy(*BUSINESS_KEY_COLUMNS)
        .count()
        .filter(F.col("count") > 1)
        .limit(1)
        .count()
    )

    if duplicate_count > 0:

        logger.error(
            "Duplicate business keys detected."
        )

        raise ValueError(
            "Duplicate records detected for frozen "
            "business grain: "
            f"{BUSINESS_KEY_COLUMNS}"
        )

    logger.info(
        "Business-key uniqueness validation successful."
    )


# ==========================================================
# Row Count Validation
# ==========================================================

def validate_row_count(
    dataframe: DataFrame
) -> None:
    """
    Ensures that the source DataFrame is not empty.

    Parameters
    ----------
    dataframe : DataFrame
        Input source DataFrame.

    Raises
    ------
    ValueError
        If no records are present.
    """

    row_count = dataframe.limit(1).count()

    if row_count == 0:

        logger.error(
            "Source dataset contains no records."
        )

        raise ValueError(
            "Source dataset is empty."
        )

    logger.info(
        "Source dataset contains records."
    )


# ==========================================================
# Complete Bronze Validation
# ==========================================================

def validate_bronze_source(
    dataframe: DataFrame
) -> bool:
    """
    Executes all Bronze source validations.

    Validation order
    ----------------
    1. Row count
    2. Columns
    3. Source data types
    4. Business-key NULLs
    5. Business-key uniqueness

    Parameters
    ----------
    dataframe : DataFrame
        Raw source DataFrame.

    Returns
    -------
    bool
        True when all validations succeed.

    Raises
    ------
    ValueError
        If any validation fails.
    """

    logger.info(
        "Starting Bronze source validation."
    )

    # ------------------------------------------------------
    # 1. Row Count
    # ------------------------------------------------------

    validate_row_count(
        dataframe
    )

    # ------------------------------------------------------
    # 2. Columns
    # ------------------------------------------------------

    validate_columns(
        dataframe
    )

    # ------------------------------------------------------
    # 3. Raw Source Data Types
    # ------------------------------------------------------

    validate_source_data_types(
        dataframe
    )

    # ------------------------------------------------------
    # 4. Business-Key NULLs
    # ------------------------------------------------------

    validate_business_key_nulls(
        dataframe
    )

    # ------------------------------------------------------
    # 5. Business-Key Duplicates
    # ------------------------------------------------------

    validate_business_key_duplicates(
        dataframe
    )

    logger.info(
        "Bronze source validation completed successfully."
    )

    return True