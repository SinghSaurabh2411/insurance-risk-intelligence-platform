"""
==========================================================
Project : Insurance Risk Intelligence Platform
Module  : Logger Utility
Author  : Saurabh Singh

Description
-----------
Creates and returns logger instances used across
the Insurance Risk Intelligence Platform.

Responsibilities
----------------
1. Create logger object
2. Create module specific log file
3. Configure console logging
4. Configure rotating file logging
5. Prevent duplicate handlers

==========================================================
"""

import logging
#from logging.handlers import TimedRotatingFileHandler
from concurrent_log_handler import ConcurrentRotatingFileHandler
from pathlib import Path

from config.logging_config import (
    LOG_FORMAT,
    DATE_FORMAT,
    LOG_LEVEL,
    LOG_FILE_NAME,
    LOG_ROTATION_WHEN,
    LOG_ROTATION_INTERVAL,
    LOG_BACKUP_COUNT,
    LOG_ENCODING,
    BRONZE_LOG_DIR,
    SILVER_LOG_DIR,
    GOLD_LOG_DIR,
    AIRFLOW_LOG_DIR,
    API_LOG_DIR
)


# ==========================================================
# Layer Directory Mapping
# ==========================================================

LOG_DIRECTORY_MAP = {

    "bronze": BRONZE_LOG_DIR,

    "silver": SILVER_LOG_DIR,

    "gold": GOLD_LOG_DIR,

    "airflow": AIRFLOW_LOG_DIR,

    "api": API_LOG_DIR

}


# ==========================================================
# Get Logger
# ==========================================================

def get_logger(
        layer: str,
        module_name: str
) -> logging.Logger:
    """
    Returns a configured logger.

    Parameters
    ----------
    layer : str
        bronze / silver / gold / airflow / api

    module_name : str
        Name of python module

    Returns
    -------
    logging.Logger
    """

    layer = layer.lower()

    if layer not in LOG_DIRECTORY_MAP:

        raise ValueError(
            f"Invalid logging layer : {layer}"
        )

    logger_name = f"{layer}.{module_name}"

    logger = logging.getLogger(logger_name)

    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    logger.propagate = False

    log_directory = LOG_DIRECTORY_MAP[layer]

    log_file = log_directory / f"{module_name}.log"

    formatter = logging.Formatter(
        LOG_FORMAT,
        DATE_FORMAT
    )

    # ======================================================
    # Console Handler
    # ======================================================

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    console_handler.setLevel(LOG_LEVEL)

    # ======================================================
    # File Handler
    # ======================================================

    # file_handler = TimedRotatingFileHandler(
    #
    #     filename=log_file,
    #
    #     when=LOG_ROTATION_WHEN,
    #
    #     interval=LOG_ROTATION_INTERVAL,
    #
    #     backupCount=LOG_BACKUP_COUNT,
    #
    #     encoding=LOG_ENCODING
    #
    # )



    file_handler = ConcurrentRotatingFileHandler(
        filename=log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB per log file
        backupCount=LOG_BACKUP_COUNT,
        use_gzip=True,  # compress old logs
        encoding=LOG_ENCODING
    )

    file_handler.setFormatter(formatter)

    file_handler.setLevel(LOG_LEVEL)

    # ======================================================
    # Attach Handlers
    # ======================================================

    logger.addHandler(console_handler)

    logger.addHandler(file_handler)

    return logger