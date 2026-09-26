import sys

from config.config import PROJECT_NAME
from utils.spark_session import create_spark_session
import logging
from bronze.bronze_loader import run_bronze_pipeline
from silver.silver_loader import run_silver_pipeline

logger = logging.getLogger("application.main")


def main() -> int:
    spark = None
    try:
        logger.info("Starting %s", PROJECT_NAME)
        spark = create_spark_session()
        run_bronze_pipeline(spark=spark)
        run_silver_pipeline(spark=spark)
        logger.info("Application completed successfully.")
        return 0
    except Exception as exception:
        logger.exception("Application execution failed: %s", str(exception))
        return 1
    finally:
        if spark is not None:
            spark.stop()


if __name__ == "__main__":
    sys.exit(main())
