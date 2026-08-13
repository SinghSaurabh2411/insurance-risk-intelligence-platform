"""
==========================================================
Project : Insurance Risk Intelligence Platform
Module  : Logging Configuration
Author  : Saurabh Singh

Description
-----------
Central logging configuration for the Insurance Risk
Intelligence Platform.

Responsibilities
----------------
1. Define log directories
2. Define logging format
3. Define logging level
4. Configure logging handlers

This module DOES NOT create logger objects.

Logger instances are created in:
utils/logger.py

==========================================================
"""

from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler

# ==========================================================
# Project Root
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ==========================================================
# Logs Root Directory
# ==========================================================

LOG_ROOT = PROJECT_ROOT / "logs"

# ==========================================================
# Layer-wise Log Directories
# ==========================================================

BRONZE_LOG_DIR = LOG_ROOT / "bronze"

SILVER_LOG_DIR = LOG_ROOT / "silver"

GOLD_LOG_DIR = LOG_ROOT / "gold"

AIRFLOW_LOG_DIR = LOG_ROOT / "airflow"

API_LOG_DIR = LOG_ROOT / "api"

# ==========================================================
# Create Directories
# ==========================================================

for directory in [
    LOG_ROOT,
    BRONZE_LOG_DIR,
    SILVER_LOG_DIR,
    GOLD_LOG_DIR,
    AIRFLOW_LOG_DIR,
    API_LOG_DIR
]:
    directory.mkdir(parents=True, exist_ok=True)

# ==========================================================
# Logging Format
# ==========================================================

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(filename)s:%(lineno)d | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ==========================================================
# Logging Level
# ==========================================================

LOG_LEVEL = logging.INFO

# ==========================================================
# Log File Settings
# ==========================================================

LOG_FILE_NAME = "application.log"

LOG_ROTATION_WHEN = "midnight"

LOG_ROTATION_INTERVAL = 1

LOG_BACKUP_COUNT = 30

LOG_ENCODING = "utf-8"

# ==========================================================
# Default Logging Configuration
# ==========================================================

LOGGING_CONFIG = {

    "version": 1,

    "disable_existing_loggers": False,

    "formatters": {

        "standard": {

            "format": LOG_FORMAT,

            "datefmt": DATE_FORMAT

        }

    },

    "handlers": {

        "console": {

            "class": "logging.StreamHandler",

            "formatter": "standard",

            "level": LOG_LEVEL

        }

    },

    "root": {

        "handlers": ["console"],

        "level": LOG_LEVEL

    }

}