"""
===============================================================================
Project : Insurance Risk Intelligence Platform
File    : config.py
Purpose : Project-wide constants
===============================================================================

This module contains ONLY project-wide constants.

It does NOT contain:
    - Oracle credentials
    - Oracle connection configuration
    - Spark configuration
    - Logging configuration
    - Business transformation logic
    - SQL execution logic

Oracle connectivity:
    src/config/oracle_config.py

Logging configuration:
    src/config/logging_config.py

Spark configuration:
    src/utils/spark_session.py

===============================================================================
"""

from pathlib import Path


# =============================================================================
# PROJECT INFORMATION
# =============================================================================

PROJECT_NAME = "Insurance Risk Intelligence Platform"

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# =============================================================================
# DIRECTORY STRUCTURE
# =============================================================================

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

LOG_DIR = PROJECT_ROOT / "logs"

SQL_DIR = PROJECT_ROOT / "oracle"


# =============================================================================
# BRONZE SOURCE DIRECTORIES
# =============================================================================

BRONZE_SOURCE_DIRECTORY = RAW_DATA_DIR

BRONZE_PROCESSED_DIRECTORY = PROCESSED_DATA_DIR / "bronze"


# =============================================================================
# SOURCE FILE CONFIGURATION
# =============================================================================

SOURCE_FILE_EXTENSION = ".csv"

CSV_DELIMITER = ","

CSV_HAS_HEADER = True


# =============================================================================
# SOURCE DATA FORMAT
# =============================================================================

# Frozen source date format confirmed from the actual dataset.
#
# Example:
#     15-06-1993
#     20-12-2017
#
# Spark DateType representation:
#     1993-06-15
#     2017-12-20

SOURCE_DATE_FORMAT = "dd-MM-yyyy"


# =============================================================================
# SCHEMA NAMES
# =============================================================================
#
# These schema names are FROZEN.
#
# DWH_CONTROL
# DWH_BRONZE
# DWH_SILVER
# DWH_GOLD
#
# =============================================================================

CONTROL_SCHEMA = "DWH_CONTROL"

BRONZE_SCHEMA = "DWH_BRONZE"

SILVER_SCHEMA = "DWH_SILVER"

GOLD_SCHEMA = "DWH_GOLD"


# =============================================================================
# CONTROL OBJECTS
# =============================================================================

CONTROL_TABLE = "ETL_CONTROL"

LOAD_SEQUENCE = "SEQ_LOAD_ID"


# Fully qualified control objects

CONTROL_TABLE_FQN = (
    f"{CONTROL_SCHEMA}.{CONTROL_TABLE}"
)

LOAD_SEQUENCE_FQN = (
    f"{CONTROL_SCHEMA}.{LOAD_SEQUENCE}"
)


# =============================================================================
# BRONZE OBJECTS
# =============================================================================

BRONZE_POLICY_TABLE = "BRONZE_POLICY_DATA"


# Fully qualified Bronze table

BRONZE_POLICY_TABLE_FQN = (
    f"{BRONZE_SCHEMA}.{BRONZE_POLICY_TABLE}"
)


# =============================================================================
# SILVER OBJECTS
# =============================================================================
#
# These are project-wide names reserved for the Silver layer.
# They will be implemented when we reach the Silver phase.
#
# =============================================================================

SILVER_CUSTOMER_TABLE = "SILVER_CUSTOMER"

SILVER_POLICY_TABLE = "SILVER_POLICY"

SILVER_PRODUCT_TABLE = "SILVER_PRODUCT"

SILVER_CHANNEL_TABLE = "SILVER_CHANNEL"


# Fully qualified Silver tables

SILVER_CUSTOMER_TABLE_FQN = (
    f"{SILVER_SCHEMA}.{SILVER_CUSTOMER_TABLE}"
)

SILVER_POLICY_TABLE_FQN = (
    f"{SILVER_SCHEMA}.{SILVER_POLICY_TABLE}"
)

SILVER_PRODUCT_TABLE_FQN = (
    f"{SILVER_SCHEMA}.{SILVER_PRODUCT_TABLE}"
)

SILVER_CHANNEL_TABLE_FQN = (
    f"{SILVER_SCHEMA}.{SILVER_CHANNEL_TABLE}"
)


# =============================================================================
# GOLD DIMENSIONS
# =============================================================================

DIM_CUSTOMER = "DIM_CUSTOMER"

DIM_POLICY = "DIM_POLICY"

DIM_PRODUCT = "DIM_PRODUCT"

DIM_CHANNEL = "DIM_CHANNEL"

DIM_TIME = "DIM_TIME"


# Fully qualified Gold dimensions

DIM_CUSTOMER_FQN = (
    f"{GOLD_SCHEMA}.{DIM_CUSTOMER}"
)

DIM_POLICY_FQN = (
    f"{GOLD_SCHEMA}.{DIM_POLICY}"
)

DIM_PRODUCT_FQN = (
    f"{GOLD_SCHEMA}.{DIM_PRODUCT}"
)

DIM_CHANNEL_FQN = (
    f"{GOLD_SCHEMA}.{DIM_CHANNEL}"
)

DIM_TIME_FQN = (
    f"{GOLD_SCHEMA}.{DIM_TIME}"
)


# =============================================================================
# GOLD FACT TABLES
# =============================================================================

FACT_POLICY = "FACT_POLICY"

FACT_CLAIMS = "FACT_CLAIMS"


# Fully qualified Gold fact tables

FACT_POLICY_FQN = (
    f"{GOLD_SCHEMA}.{FACT_POLICY}"
)

FACT_CLAIMS_FQN = (
    f"{GOLD_SCHEMA}.{FACT_CLAIMS}"
)


# =============================================================================
# BUSINESS GRAIN
# =============================================================================
#
# Frozen business grain of the source policy dataset.
#
# NOTE:
# Source dataset column names are case-sensitive from the
# application's perspective, so we use the exact source
# column names here.
#
# =============================================================================

BUSINESS_KEY = [
    "ID_policy",
    "ID_insured",
    "period"
]


# =============================================================================
# AUDIT COLUMNS
# =============================================================================

AUDIT_COLUMNS = [
    "LOAD_ID",
    "LOAD_TIMESTAMP",
    "SOURCE_FILE",
    "RECORD_HASH",
    "ETL_CREATED_BY"
]


# =============================================================================
# ETL LOAD STATUS
# =============================================================================
#
# Lifecycle:
#
# RUNNING
#    ↓
# SUCCESS
#
# RUNNING
#    ↓
# FAILED
#
# SKIPPED
#    → file was intentionally not processed
#
# =============================================================================

STATUS_RUNNING = "RUNNING"

STATUS_SUCCESS = "SUCCESS"

STATUS_FAILED = "FAILED"

STATUS_SKIPPED = "SKIPPED"


# =============================================================================
# ETL CONSTANTS
# =============================================================================

HASH_ALGORITHM = "SHA2_256"

ETL_CREATED_BY = "PYSPARK_ETL"

INCREMENTAL_LOAD = True


# =============================================================================
# FILE PROCESSING
# =============================================================================

# Only files having the configured source extension are considered
# for Bronze ingestion.

PROCESS_SOURCE_FILES = True


# =============================================================================
# JDBC WRITE CONFIGURATION
# =============================================================================

# Bronze persistence is performed through Oracle JDBC.

BRONZE_WRITE_MODE = "append"


# =============================================================================
# END OF FILE
# =============================================================================