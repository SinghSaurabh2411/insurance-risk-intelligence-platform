"""
==========================================================
Project : Insurance Risk Intelligence Platform
Module  : Oracle Configuration
Author  : Saurabh Singh

Description
-----------
Reads Oracle Database connection parameters from the
environment (.env).

This module ONLY contains Oracle connectivity.

Responsibilities
----------------
1. Oracle Server Configuration
2. JDBC Configuration
3. Schema Names
4. Schema-wise JDBC Connection Properties

No business logic should exist here.

==========================================================
"""

import os

from dotenv import load_dotenv

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

# ==========================================================
# Oracle Server Configuration
# ==========================================================

ORACLE_HOST = os.getenv("ORACLE_HOST")

ORACLE_PORT = os.getenv("ORACLE_PORT")

ORACLE_SERVICE = os.getenv("ORACLE_SERVICE")

# ==========================================================
# JDBC Driver
# ==========================================================

JDBC_DRIVER = "oracle.jdbc.driver.OracleDriver"

# ==========================================================
# JDBC URL
# ==========================================================

JDBC_URL = (
    f"jdbc:oracle:thin:@//{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}"
)

# ==========================================================
# Oracle Schemas
# ==========================================================

CONTROL_SCHEMA = "DWH_CONTROL"

BRONZE_SCHEMA = "DWH_BRONZE"

SILVER_SCHEMA = "DWH_SILVER"

GOLD_SCHEMA = "DWH_GOLD"

# ==========================================================
# Bronze JDBC Properties
# ==========================================================

BRONZE_JDBC_PROPERTIES = {
    "user": os.getenv("BRONZE_USER"),
    "password": os.getenv("BRONZE_PASSWORD"),
    "driver": JDBC_DRIVER
}

# ==========================================================
# Silver JDBC Properties
# ==========================================================

SILVER_JDBC_PROPERTIES = {
    "user": os.getenv("SILVER_USER"),
    "password": os.getenv("SILVER_PASSWORD"),
    "driver": JDBC_DRIVER
}

# ==========================================================
# Gold JDBC Properties
# ==========================================================

GOLD_JDBC_PROPERTIES = {
    "user": os.getenv("GOLD_USER"),
    "password": os.getenv("GOLD_PASSWORD"),
    "driver": JDBC_DRIVER
}

# ==========================================================
# Control JDBC Properties
# ==========================================================

CONTROL_JDBC_PROPERTIES = {
    "user": os.getenv("CONTROL_USER"),
    "password": os.getenv("CONTROL_PASSWORD"),
    "driver": JDBC_DRIVER
}