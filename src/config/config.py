"""
===============================================================================
Project : Insurance Risk Intelligence Platform
File    : config.py
Purpose : Project-wide constants
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
# SOURCE FILES
# =============================================================================

SOURCE_FILE_EXTENSION = ".csv"

SOURCE_DATE_FORMAT = "dd/MM/yyyy"

CSV_DELIMITER = ","

CSV_HAS_HEADER = True

# =============================================================================
# SCHEMA NAMES (Frozen)
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

# =============================================================================
# BRONZE TABLES
# =============================================================================

BRONZE_POLICY_TABLE = "BRONZE_POLICY_DATA"

# =============================================================================
# SILVER TABLES
# =============================================================================

SILVER_CUSTOMER_TABLE = "SILVER_CUSTOMER"

SILVER_POLICY_TABLE = "SILVER_POLICY"

SILVER_PRODUCT_TABLE = "SILVER_PRODUCT"

SILVER_CLAIMS_TABLE = "SILVER_CLAIMS"

SILVER_ENRICHMENT_TABLE = "SILVER_ENRICHMENT"

# =============================================================================
# GOLD DIMENSIONS
# =============================================================================

DIM_CUSTOMER = "DIM_CUSTOMER"

DIM_POLICY = "DIM_POLICY"

DIM_PRODUCT = "DIM_PRODUCT"

DIM_CHANNEL = "DIM_CHANNEL"

DIM_TIME = "DIM_TIME"

# =============================================================================
# GOLD FACT TABLES
# =============================================================================

FACT_POLICY = "FACT_POLICY"

FACT_CLAIMS = "FACT_CLAIMS"

# =============================================================================
# BUSINESS GRAIN (Frozen)
# =============================================================================

BUSINESS_KEY = [
    "ID_POLICY",
    "ID_INSURED",
    "PERIOD"
]

# =============================================================================
# AUDIT COLUMNS (Frozen)
# =============================================================================

AUDIT_COLUMNS = [
    "LOAD_ID",
    "LOAD_TIMESTAMP",
    "SOURCE_FILE",
    "RECORD_HASH",
    "ETL_CREATED_BY"
]

# =============================================================================
# LOAD STATUS
# =============================================================================

STATUS_STARTED = "STARTED"

STATUS_COMPLETED = "COMPLETED"

STATUS_FAILED = "FAILED"

STATUS_SKIPPED = "SKIPPED"

# =============================================================================
# ETL CONSTANTS
# =============================================================================

HASH_ALGORITHM = "SHA2_256"

ETL_CREATED_BY = "PYSPARK_ETL"

INCREMENTAL_LOAD = True

MERGE_STRATEGY = "ORACLE_MERGE"

# =============================================================================
# END OF FILE
# =============================================================================