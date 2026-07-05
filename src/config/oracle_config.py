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

==========================================================
"""

import os

from dotenv import load_dotenv

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

# ==========================================================
# Oracle Server
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
# Bronze Connection
# ==========================================================

BRONZE_PROPERTIES = {
    "user": os.getenv("BRONZE_USER"),
    "password": os.getenv("BRONZE_PASSWORD"),
    "driver": JDBC_DRIVER
}

# ==========================================================
# Silver Connection
# ==========================================================

SILVER_PROPERTIES = {
    "user": os.getenv("SILVER_USER"),
    "password": os.getenv("SILVER_PASSWORD"),
    "driver": JDBC_DRIVER
}

# ==========================================================
# Gold Connection
# ==========================================================

GOLD_PROPERTIES = {
    "user": os.getenv("GOLD_USER"),
    "password": os.getenv("GOLD_PASSWORD"),
    "driver": JDBC_DRIVER
}

# ==========================================================
# Control Connection
# ==========================================================

CONTROL_PROPERTIES = {
    "user": os.getenv("CONTROL_USER"),
    "password": os.getenv("CONTROL_PASSWORD"),
    "driver": JDBC_DRIVER
}