"""
==========================================================
Project : Insurance Risk Intelligence Platform
Module  : File Handler
Author  : Saurabh Singh

Description
-----------
Provides reusable functions for discovering and selecting
source files for the ETL pipeline.

Responsibilities
----------------
1. Discover source files.
2. Filter supported file types.
3. Return files that are eligible for processing.
4. Prevent already successfully processed files from
   being selected again.

This module contains NO transformation logic and NO
Oracle database logic.

==========================================================
"""

from pathlib import Path
from typing import List


from utils.control_table import (
    is_file_processed
)

from utils.logger import get_logger


# ==========================================================
# Logger
# ==========================================================

logger = get_logger(
    layer="bronze",
    module_name="file_handler"
)


# ==========================================================
# Supported File Extensions
# ==========================================================

SUPPORTED_EXTENSIONS = {
    ".csv"
}


# ==========================================================
# Discover Source Files
# ==========================================================

def discover_source_files(
    source_directory: str
) -> List[Path]:
    """
    Discovers supported source files from the supplied
    directory.

    Parameters
    ----------
    source_directory : str
        Directory containing source files.

    Returns
    -------
    List[Path]
        List of discovered supported files.
    """

    source_path = Path(source_directory)

    if not source_path.exists():

        raise FileNotFoundError(
            f"Source directory does not exist: "
            f"{source_directory}"
        )

    if not source_path.is_dir():

        raise NotADirectoryError(
            f"Source path is not a directory: "
            f"{source_directory}"
        )

    logger.info(
        "Scanning source directory: %s",
        source_path
    )

    files = [
        file
        for file in source_path.iterdir()
        if (
            file.is_file()
            and file.suffix.lower()
            in SUPPORTED_EXTENSIONS
        )
    ]

    files.sort(
        key=lambda file: file.name
    )

    logger.info(
        "Discovered %d supported source file(s).",
        len(files)
    )

    return files


# ==========================================================
# Get Unprocessed Files
# ==========================================================

def get_unprocessed_files(
    source_directory: str
) -> List[Path]:
    """
    Returns source files that have not been successfully
    processed according to the ETL control table.

    Parameters
    ----------
    source_directory : str
        Directory containing source files.

    Returns
    -------
    List[Path]
        Files eligible for processing.
    """

    source_files = discover_source_files(
        source_directory
    )

    unprocessed_files = []

    for file_path in source_files:

        source_file = file_path.name

        if is_file_processed(source_file):

            logger.info(
                "Skipping already processed file: %s",
                source_file
            )

            continue

        logger.info(
            "File eligible for processing: %s",
            source_file
        )

        unprocessed_files.append(
            file_path
        )

    logger.info(
        "Total unprocessed files: %d",
        len(unprocessed_files)
    )

    return unprocessed_files


# ==========================================================
# Get Latest Unprocessed File
# ==========================================================

def get_latest_unprocessed_file(
    source_directory: str
):
    """
    Returns the latest unprocessed source file.

    Files are ordered by modification time.

    Parameters
    ----------
    source_directory : str
        Directory containing source files.

    Returns
    -------
    Path or None
        Latest eligible file.
    """

    unprocessed_files = get_unprocessed_files(
        source_directory
    )

    if not unprocessed_files:

        logger.info(
            "No unprocessed source files found."
        )

        return None

    latest_file = max(
        unprocessed_files,
        key=lambda file: file.stat().st_mtime
    )

    logger.info(
        "Latest unprocessed file: %s",
        latest_file.name
    )

    return latest_file