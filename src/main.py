import sys
import logging

from config.config import PROJECT_NAME
from orchestration.pipeline import run_pipeline

logger = logging.getLogger("application.main")


def main() -> int:
    try:
        logger.info("Starting %s", PROJECT_NAME)
        run_pipeline()
        logger.info("Application completed successfully.")
        return 0
    except Exception as exception:
        logger.exception("Application execution failed: %s", str(exception))
        return 1


if __name__ == "__main__":
    sys.exit(main())
