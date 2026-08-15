"""
==========================================================
Project : Insurance Risk Intelligence Platform
Module  : Hash Generator
Author  : Saurabh Singh

Description
-----------
Provides reusable functions for generating deterministic
record hashes for the ETL pipeline.

Hash Strategy
-------------
The RECORD_HASH is generated from the complete set of
business/data columns supplied to the function.

The business key:

    ID_policy
    ID_insured
    period

is NOT used as the sole basis for RECORD_HASH.

This allows the ETL pipeline to detect changes in any
business attribute while maintaining the frozen record
grain.

Responsibilities
----------------
1. Generate deterministic record hash
2. Generate hash column in Spark DataFrame
3. Handle NULL values consistently
4. Preserve deterministic column ordering

No ETL business logic should exist here.

==========================================================
"""

from typing import List

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from utils.logger import get_logger


# ==========================================================
# Logger
# ==========================================================

logger = get_logger(
    layer="bronze",
    module_name="hash_generator"
)


# ==========================================================
# Generate Record Hash
# ==========================================================

def add_record_hash(
    dataframe: DataFrame,
    columns: List[str],
    hash_column: str = "RECORD_HASH"
) -> DataFrame:
    """
    Adds a deterministic SHA-256 record hash to a
    Spark DataFrame.

    Parameters
    ----------
    dataframe : DataFrame
        Input Spark DataFrame.

    columns : List[str]
        Complete set of business/data columns that should
        participate in the record hash.

    hash_column : str
        Name of the generated hash column.

        Default:
        RECORD_HASH

    Returns
    -------
    DataFrame
        DataFrame containing the generated hash column.

    Notes
    -----
    NULL values are converted to a consistent placeholder
    before hashing.

    The column order supplied to `columns` must remain
    consistent across ETL executions.
    """

    if not columns:

        raise ValueError(
            "Hash column list cannot be empty."
        )

    missing_columns = [
        column
        for column in columns
        if column not in dataframe.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Columns not found in DataFrame: "
            f"{missing_columns}"
        )

    logger.info(
        "Generating %s using %d columns.",
        hash_column,
        len(columns)
    )

    # ======================================================
    # Normalize Values
    # ======================================================

    normalized_columns = [

        F.coalesce(
            F.col(column).cast("string"),
            F.lit("<NULL>")
        )

        for column in columns

    ]

    # ======================================================
    # Generate Deterministic Hash
    # ======================================================

    hashed_dataframe = dataframe.withColumn(

        hash_column,

        F.sha2(

            F.concat_ws(
                "||",
                *normalized_columns
            ),

            256

        )

    )

    logger.info(
        "Successfully generated %s.",
        hash_column
    )

    return hashed_dataframe